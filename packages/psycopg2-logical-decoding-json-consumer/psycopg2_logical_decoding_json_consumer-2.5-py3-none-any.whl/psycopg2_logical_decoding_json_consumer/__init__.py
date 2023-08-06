#   Copyright 2019, 2020 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import asyncio
import json

import psycopg2
import psycopg2.extras

REPLICATION_STATUS_INTERVAL = 15


class Consumer:
    def __init__(self, dsn, slot_name, event_filter=None):
        self._dsn = dsn
        self._slot_name = slot_name
        self._event_filter = event_filter

        self._current_transaction_events = None
        self._unflushed_transactions = []

        self._current_batch_transactions = []

    def __repr__(self):
        info = [self.__class__.__name__]

        info.append(f"dsn={self._dsn}")
        info.append(f"slot_name={self._slot_name}")
        info.append(f"current_transaction_events={self._current_transaction_events}")
        info.append(f"unflushed_transactions={self._unflushed_transactions}")

        return "<{}>".format(" ".join(info))

    async def connect(self):
        loop = asyncio.get_running_loop()

        await loop.run_in_executor(None, self._connect)

    async def close(self):
        loop = asyncio.get_running_loop()

        await loop.run_in_executor(None, self._close)

    async def read_transaction(self):
        while True:
            replication_message = self._cursor.read_message()

            if replication_message is None:
                # If we're not collecting events within a transaction and
                # there are no unflushed transactions, we can advance
                # to the most recent (presumably keepalive) message.
                # This helps with the lag calculations in pg_stat_replication
                if self._current_transaction_events is None and not self._unflushed_transactions:
                    self._advance_applied_lsn(self._cursor.wal_end)

                await self._wait_until_readable_or_timeout()
                continue

            event = json.loads(replication_message.payload)

            if self._current_transaction_events is None:
                if event['kind'] == "message":
                    # Message sent with Transactional=False
                    txn = self._construct_transaction([event], replication_message.data_start)

                    # txn will be None if, after filtering, it contained no
                    # events (in which case construct_transaction will take care
                    # of marking it as applied)
                    if txn:
                        return txn
                elif event['kind'] == "begin":
                    self._current_transaction_events = []
                else:
                    raise ProtocolError(f"Message unexpectedly arrived outside of a transaction: {replication_message!r}")

            else:
                if event['kind'] == "commit":
                    txn = self._construct_transaction(self._current_transaction_events, replication_message.data_start)
                    self._current_transaction_events = None

                    # txn will be None if, after filtering, it contained no
                    # events (in which case construct_transaction will take care
                    # of marking it as applied)
                    if txn:
                        return txn
                elif event['kind'] in ("change", "truncate", "message"):
                    self._current_transaction_events.append(event)
                else:
                    raise ProtocolError(f"Message unexpectedly arrived inside a transaction: {replication_message!r}")

    async def read_transaction_batch(self, max_gather_count=None, max_gather_time=None):
        loop = asyncio.get_running_loop()

        if not max_gather_count and not max_gather_time:
            raise RuntimeError("Unlimited transaction batch would never return, supply at least one of max_gather_count or max_gather_time")

        while True:
            if max_gather_count and len(self._current_batch_transactions) >= max_gather_count:
                txns = self._current_batch_transactions[:max_gather_count]
                self._current_batch_transactions = self._current_batch_transactions[max_gather_count:]
                return txns

            if max_gather_time and self._current_batch_transactions:
                read_transaction_timeout = self._current_batch_transactions[0]._arrival_time + max_gather_time - loop.time()
                if read_transaction_timeout <= 0:
                    txns = self._current_batch_transactions
                    self._current_batch_transactions = []
                    return txns
            else:
                read_transaction_timeout = None

            try:
                txn = await asyncio.wait_for(self.read_transaction(), read_transaction_timeout)
            except asyncio.TimeoutError:
                pass
            else:
                self._current_batch_transactions.append(txn)

    async def send_feedback(self):
        loop = asyncio.get_running_loop()

        await loop.run_in_executor(None, self._send_feedback)

    def _connect(self):
        self._connection = psycopg2.connect(self._dsn, connection_factory=psycopg2.extras.LogicalReplicationConnection)
        self._cursor = self._connection.cursor()

        self._cursor.start_replication(slot_name=self._slot_name, decode=True, status_interval=REPLICATION_STATUS_INTERVAL)

    def _close(self):
        self._connection.close()

    # use of future inspired by asyncio.selector_events.BaseSelectorEventLoop.sock_recv
    async def _wait_until_readable_or_timeout(self):
        loop = asyncio.get_running_loop()

        fut = loop.create_future()
        fd = self._connection.fileno()

        loop.add_reader(fd, self._socket_readable, fd, fut)

        try:
            await asyncio.wait_for(fut, REPLICATION_STATUS_INTERVAL)
        except asyncio.TimeoutError:
            pass
        finally:
            loop.remove_reader(fd)

    def _socket_readable(self, fd, fut):
        # fut may be cancelled by wait_for just before we are called
        if fut.cancelled():
            return

        loop = asyncio.get_running_loop()

        loop.remove_reader(fd)
        fut.set_result(None)

    def _construct_transaction(self, events, commit_lsn):
        loop = asyncio.get_running_loop()

        if self._event_filter:
            events = list(filter(self._event_filter, events))

        # We always generate a Transaction even if we're about to mark it
        # applied so it can be tracked by unflushed_transactions
        txn = Transaction(self, events, commit_lsn, loop.time())
        self._unflushed_transactions.append(txn)

        # Quietly mark the transaction as applied if it's empty
        if events:
            return txn
        else:
            txn.applied()

    def _advance_applied_lsn(self, lsn):
        # Update all three LSNs to make pg_stat_replication clearer
        # This will never block
        self._cursor.send_feedback(write_lsn=lsn, flush_lsn=lsn, apply_lsn=lsn, force=False)

    def _send_feedback(self):
        # This might block
        self._cursor.send_feedback(force=True)

    def _transaction_became_flushable(self, txn):
        txn_idx = self._unflushed_transactions.index(txn)

        # If the transaction before this newly flushable transaction is already
        # flushable, discard the earlier transaction because we can now flush
        # beyond it.
        if txn_idx > 0:
            previous_txn_idx = txn_idx-1
            previous_txn = self._unflushed_transactions[previous_txn_idx]

            if previous_txn._flushable:
                del self._unflushed_transactions[previous_txn_idx]
                txn_idx = previous_txn_idx

        # If the transaction after this newly flushable transaction is
        # already flushable, discard the current transaction because we can
        # flush beyond it.
        if txn_idx < len(self._unflushed_transactions)-1:
            next_txn = self._unflushed_transactions[txn_idx+1]
            if next_txn._flushable:
                del self._unflushed_transactions[txn_idx]
                txn_idx = None

        earliest_unflushed_txn = self._unflushed_transactions[0]

        if earliest_unflushed_txn._flushable:
            del self._unflushed_transactions[0]

            self._advance_applied_lsn(earliest_unflushed_txn._commit_lsn)


class ProtocolError(Exception):
    pass


class Transaction:
    def __init__(self, consumer, events, commit_lsn, arrival_time):
        self.consumer = consumer
        self.events = events
        self._commit_lsn = commit_lsn
        self._arrival_time = arrival_time
        self._flushable = False

    def __repr__(self):
        info = [self.__class__.__name__]

        info.append(f"events={self.events}")
        info.append(f"commit_lsn={lsn_int_to_str(self._commit_lsn)}")
        info.append(f"arrival_time={self._arrival_time}")
        info.append(f"flushable={self._flushable}")

        return "<{}>".format(" ".join(info))

    def applied(self):
        self._flushable = True
        self.consumer._transaction_became_flushable(self)


def lsn_int_to_str(lsn):
    lsn_high = (lsn >> 32) & 0xffffffff
    lsn_low = lsn & 0xffffffff

    return "{:X}/{:X}".format(lsn_high, lsn_low)
