#!/usr/bin/env ptpython

from ptpython.repl import embed
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)
import psycopg2

# ptpython repl config:
def configure(repl):
    repl.confirm_exit = False


# lazy initialized engine provides factory and connection pool:
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost/postgres",
    echo=False,
    future=True,
)

# https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#setting-up-metadata-with-table-objects
# collection of our tables:
metadata = MetaData()

user_table = Table(
    "user_accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False),
)

message_table = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String(100), nullable=False),
    Column("by", ForeignKey("user_accounts.id"), nullable=False),
    Column("to", ForeignKey("user_accounts.id")),
)

metadata.drop_all(engine)
metadata.create_all(engine)

embed(globals(), locals(), configure=configure)
