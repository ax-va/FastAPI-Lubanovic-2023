import sqlite3
from sqlite3 import Connection

from app.config import DATABASE_FILE

conn: Connection


def init() -> None:
    create_creatures_table()
    create_explorers_table()
    conn.commit()


def connect(database_file: str = DATABASE_FILE) -> Connection:
    return sqlite3.connect(database_file, check_same_thread=False)


def disconnect() -> None:
    conn.cursor().close()
    conn.close()


def create_creatures_table() -> None:
    conn.cursor().execute(
        "CREATE TABLE IF NOT EXISTS creatures ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   area TEXT, "
        "   description TEXT, "
        "   aka TEXT"
        ")"
    )


def create_explorers_table() -> None:
    conn.cursor().execute(
        "CREATE TABLE IF NOT EXISTS explorers ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   description TEXT"
        ")"
    )


conn = connect()
