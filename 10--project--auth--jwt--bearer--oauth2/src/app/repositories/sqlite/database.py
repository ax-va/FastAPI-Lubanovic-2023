import sqlite3
from sqlite3 import Connection
from typing import Generator

from app.config import DATABASE_FILE


def init(database_file: str = DATABASE_FILE) -> None:
    connection = sqlite3.connect(
        database_file,
        check_same_thread=False,
    )

    try:
        create_creatures_table(connection)
        create_explorers_table(connection)
        create_users_table(connection)

    except Exception:
        connection.rollback()
        raise

    else:
        connection.commit()

    finally:
        connection.close()


def get_connection(
    database_file: str = DATABASE_FILE,
) -> Generator[Connection, None, None]:
    """Provides a database connection for a unit of work and close it afterwards."""
    connection = sqlite3.connect(
        database_file,
        check_same_thread=False,
    )
    connection.row_factory = sqlite3.Row

    try:
        yield connection

    finally:
        connection.close()


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