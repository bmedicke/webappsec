#!/usr/bin/env ptpython

from ptpython.repl import embed
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry

# lazy initialized engine provides factory and connection pool:
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost/postgres",
    echo=False,
    future=True,
)

# ptpython repl config:
def configure(repl):
    repl.confirm_exit = False


# the registry holds our ORM mappings:
mapper_registry = registry()

# each mapped class descends from a common base
# class known as the declarative base:
Base = mapper_registry.generate_base()


class User(Base):
    __tablename__ = "user_accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    text = Column(String(100), nullable=False)
    by = Column(ForeignKey("user_accounts.id"), nullable=False)
    to = Column(ForeignKey("user_accounts.id"))


# the registry already contains a metadata object.
mapper_registry.metadata.drop_all(engine)
mapper_registry.metadata.create_all(engine)

embed(globals(), locals(), configure=configure)
