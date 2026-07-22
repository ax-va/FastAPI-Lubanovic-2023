from sqlite3 import IntegrityError, Connection

from app.models.users import UserToDB, UserFromDB
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


def get_all(connection: Connection) -> list[UserFromDB]:
    query = "SELECT * FROM users"
    cursor = connection.cursor()
    cursor.execute(query)

    return [to_model(row) for row in cursor.fetchall()]


def get_by_id(
    connection: Connection,
    user_id: int,
) -> UserFromDB | None:
    query = "SELECT * FROM users WHERE id = :id"
    values = {"id": user_id}
    cursor = connection.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_model(row) if row else None


def get_by_username(
    connection: Connection,
    username: str,
) -> UserFromDB | None:
    query = "SELECT * FROM users WHERE username = :username"
    values = {"username": username}
    cursor = connection.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_model(row) if row else None


def create(
    connection: Connection,
    user: UserToDB,
) -> int:
    query = (
        "INSERT INTO users (username, password_hash, is_active, is_admin) "
        "VALUES (:username, :password_hash, :is_active, :is_admin)"
    )
    values = to_dict(user)
    cursor = connection.cursor()

    try:
        cursor.execute(query, values)

    except IntegrityError as e:
        message = str(e).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError(f"Username {user.username!r} already exists") from e
        raise

    created_id: int | None = cursor.lastrowid
    if created_id is None:
        raise RuntimeError(f"User ID was not returned")

    return created_id


def replace(
    connection: Connection,
    user_id: int,
    user: UserToDB,
) -> None:
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
    cursor = connection.cursor()

    try:
        cursor.execute(query, values)

    except IntegrityError as e:
        message = str(e).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError(f"Username {user.username!r} already exists") from e
        raise


def delete(
    connection: Connection,
    user_id: int,
) -> None:
    """Soft-delete a user."""
    query = (
        "UPDATE users "
        "SET is_active = FALSE "
        "WHERE id = :user_id"
    )
    values = {"user_id": user_id}
    cursor = connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise RuntimeError(f"User with ID {user_id} not deleted")


def count_admins(connection: Connection) -> int:
    query = (
        "SELECT COUNT(*)"
        "FROM users "
        "WHERE is_admin = TRUE"
    )
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    return row[0]


def set_admin(
    connection: Connection,
    user_id: int,
    is_admin: bool,
) -> None:
    query = (
        "UPDATE users "
        "SET is_admin = :is_admin "
        "WHERE id = :user_id"
    )
    values = {
        "user_id": user_id,
        "is_admin": is_admin,
    }
    cursor = connection.cursor()
    cursor.execute(query, values)
