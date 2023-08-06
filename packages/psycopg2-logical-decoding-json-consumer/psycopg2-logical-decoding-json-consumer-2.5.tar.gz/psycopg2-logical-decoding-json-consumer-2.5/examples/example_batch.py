#   Copyright 2020 University of Lancaster
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
import random

from psycopg2_logical_decoding_json_consumer import Consumer

DSN = ""
SLOT = "example"
BATCH_MAX_GATHER_COUNT = 5
BATCH_MAX_GATHER_TIME = 10


def event_filter(event):
    return event['kind'] == "change" and event['action'] == "insert"


async def main():
    consumer = Consumer(DSN, SLOT, event_filter=event_filter)
    await consumer.connect()

    while True:
        transactions = await consumer.read_transaction_batch(
            max_gather_count=BATCH_MAX_GATHER_COUNT,
            max_gather_time=BATCH_MAX_GATHER_TIME)

        asyncio.create_task(process_transactions(consumer, transactions))


async def process_transactions(consumer, transactions):
    print(f"Processing transaction batch {transactions!r}")
    await asyncio.sleep(random.randint(1, 10))
    print(f"Processed transaction batch {transactions!r}")

    for transaction in transactions:
        transaction.applied()

    # Usually the consumer will send feedback to the server every so
    # often (15 seconds by default), so if the consumer exits immediately
    # after marking a transaction as 'applied', the server may not be aware
    # and feed the same transactions when the consumer restarts.
    # If potentially repeatedly processing the same transaction has a high
    # cost manually sending feedback may be worth-while.
    await consumer.send_feedback()


asyncio.run(main())
