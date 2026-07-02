import sqlite3

DATABASE_FILE = "lubanovic.db"

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()


def init():
    create_creatures_table()
    create_explorers_table()
    conn.commit()


def create_creatures_table():
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


def create_explorers_table():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS explorers ("
        "   id INTEGER PRIMARY KEY, "
        "   name TEXT NOT NULL, "
        "   country TEXT, "
        "   description TEXT"
        ")"
    )
