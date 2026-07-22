import sqlite3
from contextlib import contextmanager
from sqlite3 import Connection
from typing import Generator

from app.config import DATABASE_FILE


@contextmanager
def connection_manager(
    database_file: str = DATABASE_FILE,
) -> Generator[Connection, None, None]:
    connection = sqlite3.connect(
        database_file,
        check_same_thread=False,
    )
    connection.row_factory = sqlite3.Row

    try:
        yield connection
    finally:
        connection.close()


def init(connection: Connection) -> None:
    try:
        create_creatures_table(connection)
        create_explorers_table(connection)
        create_users_table(connection)

    except Exception:
        connection.rollback()
        raise

    else:
        connection.commit()


def create_creatures_table(connection: Connection) -> None:
    connection.execute(
        "CREATE TABLE IF NOT EXISTS creatures ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   area TEXT, "
        "   description TEXT, "
        "   aka TEXT"
        ")"
    )


def create_explorers_table(connection: Connection) -> None:
    connection.execute(
        "CREATE TABLE IF NOT EXISTS explorers ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   description TEXT"
        ")"
    )


def create_users_table(connection: Connection) -> None:
    connection.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "   id INTEGER PRIMARY KEY, "
        "   username TEXT NOT NULL UNIQUE, "
        "   password_hash TEXT NOT NULL, "
        "   is_active BOOLEAN NOT NULL DEFAULT TRUE, "
        "   is_admin BOOLEAN NOT NULL DEFAULT FALSE"
        ")"
    )