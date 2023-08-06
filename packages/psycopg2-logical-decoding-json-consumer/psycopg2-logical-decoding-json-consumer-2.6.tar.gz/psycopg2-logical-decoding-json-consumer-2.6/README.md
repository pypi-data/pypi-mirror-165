PsycoPG2-Logical-Decoding-JSON-Consumer
=======================================

psycopg2-logical-decoding-json-consumer is an asynchronous library that consumes
PostgreSQL logical replication created by the logical-decoding-json output
plugin.

The library supports fast filtering of events and allows individual transactions
to be acknowledged out of order.

Transactions can be read one-by-one with read_transaction(), or collected in
batches (simplifying de-duplication) with read_transaction_batch()
