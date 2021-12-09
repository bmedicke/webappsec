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
# we'll use psycopg2 until 3 is supported.

create_db = """
DROP TABLE IF EXISTS test;
CREATE TABLE test (
  x INTEGER NOT NULL,
  y INTEGER NOT NULL
);
"""

# insert using bound parameters
# to avoid SQL injections:
insert_coords = """
INSERT INTO test (x, y)
VALUES (:x, :y);
"""

select_all = """
SELECT * from test;
"""

coords = [{"x": 42, "y": 0}, {"x": 8, "y": 13}, {"x": 21, "y": -2}]

# autocommit block:
# "begin once"
with engine.connect() as conn:
    conn.execute(text(create_db))
    # for DML statements we can send multiple sets of parameters:
    conn.execute(text(insert_coords), coords)
    result = conn.execute(text(select_all))
    rows = result.all()

    # tuple assignment:
    for i, (x, y) in enumerate(rows):
        print(f"row: {i}\tx: {x}, y: {y}")

    conn.commit()  # commit before repl.
    from ptpython.repl import embed

    embed(globals(), locals())
