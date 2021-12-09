#!/usr/bin/env ptpython

import psycopg2
from sqlalchemy import create_engine, text

# lazy initialized engine provides factory and connection pool:
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost/postgres",
    echo=False,
    future=True,
)
# future enables SQLAlchemy 2.0 syntax,
# echo passes all SQL queries to the python logger.
# we'll use psycopg2 until 3 ist supported.

create_db = """
DROP TABLE IF EXISTS test;
CREATE TABLE test (
  number INTEGER NOT NULL
);
"""

insert_numbers = """
INSERT INTO test (number)
VALUES (:number);
"""

select_all = """
SELECT * from test;
"""

numbers = [{"number": 42}, {"number": 8}, {"number": 21}]

# autocommit block:
# "begin once"
with engine.connect() as conn:
    conn.execute(text(create_db))
    conn.execute(text(insert_numbers), numbers)
    result = conn.execute(text(select_all))
    rows = result.all()
    for row in rows:
        from ptpython.repl import embed; embed(globals(), locals())
