import sqlite3
from contextlib import contextmanager
from sqlite3 import Connection
from typing import Generator

from app.config import DATABASE_FILE


@contextmanager
def connect(
    database_file: str = DATABASE_FILE,
) -> Generator[Connection, None, None]:
    db_connection = sqlite3.connect(
        database_file,
        check_same_thread=False,
    )
    db_connection.row_factory = sqlite3.Row

    try:
        yield db_connection
    finally:
        db_connection.close()


def init(db_connection: Connection) -> None:
    try:
        create_creatures_table(db_connection)
        create_explorers_table(db_connection)
        create_users_table(db_connection)

    except Exception:
        db_connection.rollback()
        raise

    else:
        db_connection.commit()


def create_creatures_table(db_connection: Connection) -> None:
    db_connection.execute(
        "CREATE TABLE IF NOT EXISTS creatures ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   area TEXT, "
        "   description TEXT, "
        "   aka TEXT"
        ")"
    )


def create_explorers_table(db_connection: Connection) -> None:
    db_connection.execute(
        "CREATE TABLE IF NOT EXISTS explorers ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   description TEXT"
        ")"
    )


def create_users_table(db_connection: Connection) -> None:
    db_connection.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "   id INTEGER PRIMARY KEY, "
        "   username TEXT NOT NULL UNIQUE, "
        "   password_hash TEXT NOT NULL, "
        "   is_active BOOLEAN NOT NULL DEFAULT TRUE, "
        "   is_admin BOOLEAN NOT NULL DEFAULT FALSE"
        ")"
    )