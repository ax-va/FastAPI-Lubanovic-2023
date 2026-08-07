from app.repositories.sqlite import database as db

with db.connect() as db_connection:
    db.ensure_schema_exists(db_connection)
