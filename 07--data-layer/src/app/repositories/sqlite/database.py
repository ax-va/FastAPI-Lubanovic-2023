import sqlite3
from sqlite3 import Connection, Cursor

DATABASE_FILE = "lubanovic.db"


def init() -> None:
    create_creatures_table()
    create_explorers_table()
    conn.commit()


def connect(database_file: str = DATABASE_FILE) -> tuple[Connection, Cursor]:
    conn_: Connection = sqlite3.connect(database_file)
    cursor_: Cursor = conn_.cursor()
    return conn_, cursor_


def disconnect() -> None:
    cursor.close()
    conn.close()


def create_creatures_table() -> None:
    cursor.execute(
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
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS explorers ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   description TEXT"
        ")"
    )


conn, cursor = connect()
