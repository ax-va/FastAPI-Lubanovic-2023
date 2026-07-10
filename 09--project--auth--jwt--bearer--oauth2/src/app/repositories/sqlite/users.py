from sqlite3 import IntegrityError

from app.models.users import UserToDB, UserFromDB
from . import database as db
from ..errors import DuplicateError, INTEGRITY_ERROR_UNIQUE


def to_model(row: tuple) -> UserFromDB:
    user_id, username, password_hash, is_active, is_admin = row
    return UserFromDB(
        id=user_id,
        username=username,
        password_hash=password_hash,
        is_active=is_active,
        is_admin=is_admin,
    )


def to_dict(user: UserToDB | UserFromDB) -> dict:
    return user.model_dump()


def get_by_id(user_id: int) -> UserFromDB | None:
    query = "SELECT * FROM users WHERE id = :id"
    values = {"id": user_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_model(row) if row else None


def get_by_username(username: str) -> UserFromDB | None:
    query = "SELECT * FROM users WHERE username = :username"
    values = {"username": username}
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_model(row) if row else None


def get_all() -> list[UserFromDB]:
    query = "SELECT * FROM users"
    cursor = db.conn.cursor()
    cursor.execute(query)

    return [to_model(row) for row in cursor.fetchall()]


def create(user: UserToDB) -> UserFromDB:
    query = (
        "INSERT INTO users (username, password_hash, is_active, is_admin) "
        "VALUES (:username, :password_hash, :is_active, :is_admin)"
    )
    values = to_dict(user)
    cursor = db.conn.cursor()

    try:
        cursor.execute(query, values)

    except IntegrityError as e:
        message = str(e).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError(f"Username {user.username!r} already exists") from e
        raise

    else:
        db.conn.commit()

    inserted_id: int | None = cursor.lastrowid
    if inserted_id is None:
        raise RuntimeError(f"Inserted user id was not returned")

    inserted: UserFromDB | None = get_by_id(inserted_id)
    if inserted is None:
        raise RuntimeError(f"Inserted user with id={inserted_id} could not be retrieved")

    return inserted


def replace(user_id: int, user: UserToDB) -> UserFromDB:
    query = (
        "UPDATE users "
        "SET username = :username, "
        "    password_hash = :password_hash, "
        "    is_active = :is_active,"
        "    is_admin = :is_admin "
        "WHERE id = :user_id"
    )
    values = to_dict(user)
    values["user_id"] = user_id
    cursor = db.conn.cursor()

    try:
        cursor.execute(query, values)

    except IntegrityError as e:
        message = str(e).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError(f"Username {user.username!r} already exists") from e
        raise

    else:
        db.conn.commit()

    updated: UserFromDB | None = get_by_id(user_id)
    if updated is None:
        raise RuntimeError(f"Updated user with id={user_id} could not be retrieved")

    return updated


def delete(user_id: int) -> bool:
    """Soft-delete a user."""
    query = (
        "UPDATE users "
        "SET is_active = FALSE "
        "WHERE id = :user_id"
    )
    values = {"user_id": user_id}
    cursor = db.conn.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        return False

    db.conn.commit()

    return True


def count_admins() -> int:
    query = (
        "SELECT COUNT(*)"
        "FROM users "
        "WHERE is_admin = TRUE"
    )
    cursor = db.conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    return row[0]


def set_admin(user_id: int, is_admin: bool) -> UserFromDB:
    query = (
        "UPDATE users "
        "SET is_admin = :is_admin "
        "WHERE id = :user_id"
    )
    values = {
        "user_id": user_id,
        "is_admin": is_admin,
    }
    cursor = db.conn.cursor()
    cursor.execute(query, values)
    db.conn.commit()

    updated: UserFromDB | None = get_by_id(user_id)
    if updated is None:
        raise RuntimeError(f"Updated user with id={user_id} could not be retrieved")

    return updated
