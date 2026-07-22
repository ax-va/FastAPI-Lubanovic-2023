from app.repositories.sqlite import database as db
from app.repositories.sqlite.database import connection_manager

with connection_manager() as connection:
    db.init(connection)
