from app.repositories.sqlite import database as db

with db.connect() as db_connection:
    db.init(db_connection)
