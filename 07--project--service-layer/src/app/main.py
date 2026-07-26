from app.repositories.sqlite import database as db

with db.connect() as db_connection:
    db.ensure_tables_exist(db_connection)
