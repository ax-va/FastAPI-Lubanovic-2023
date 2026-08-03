from sqlite3 import IntegrityError, Connection

from app.models.schemas.users import UserToRepo, UserFromRepo
from ..errors import DuplicateError, INTEGRITY_ERROR_UNIQUE


def to_from_repo(row: tuple) -> UserFromRepo:
    return UserFromRepo(**dict(row))


def to_dict(user: UserToRepo | UserFromRepo) -> dict:
    return user.model_dump()


def get_all(db_connection: Connection) -> list[UserFromRepo]:
    query = "SELECT * FROM users"
    cursor = db_connection.cursor()
    cursor.execute(query)

    return [to_from_repo(row) for row in cursor.fetchall()]


def get_by_id(
    db_connection: Connection,
    user_id: int,
) -> UserFromRepo | None:
    query = "SELECT * FROM users WHERE id = :id"
    values = {"id": user_id}
    cursor = db_connection.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_from_repo(row) if row else None


def get_by_username(
    db_connection: Connection,
    username: str,
) -> UserFromRepo | None:
    query = "SELECT * FROM users WHERE username = :username"
    values = {"username": username}
    cursor = db_connection.cursor()
    cursor.execute(query, values)
    row = cursor.fetchone()

    return to_from_repo(row) if row else None


def create(
    db_connection: Connection,
    user_to_repo: UserToRepo,
) -> int:
    query = (
        "INSERT INTO users (username, password_hash, is_active, is_admin) "
        "VALUES (:username, :password_hash, :is_active, :is_admin)"
    )
    values = to_dict(user_to_repo)
    cursor = db_connection.cursor()

    try:
        cursor.execute(query, values)

    except IntegrityError as e:
        message = str(e).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError(f"Username {user_to_repo.username!r} already exists") from e
        raise

    created_id: int | None = cursor.lastrowid
    if created_id is None:
        raise RuntimeError(f"User ID was not returned")

    return created_id


def replace(
    db_connection: Connection,
    user_id: int,
    user_to_repo: UserToRepo,
) -> None:
    query = (
        "UPDATE users "
        "SET username = :username, "
        "    password_hash = :password_hash, "
        "    is_active = :is_active,"
        "    is_admin = :is_admin "
        "WHERE id = :user_id"
    )
    values = to_dict(user_to_repo)
    values["user_id"] = user_id
    cursor = db_connection.cursor()

    try:
        cursor.execute(query, values)

    except IntegrityError as e:
        message = str(e).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError(f"Username {user_to_repo.username!r} already exists") from e
        raise


def soft_delete(
    db_connection: Connection,
    user_id: int,
) -> None:
    """Soft-delete a user."""
    query = (
        "UPDATE users "
        "SET is_active = FALSE "
        "WHERE id = :user_id"
    )
    values = {"user_id": user_id}
    cursor = db_connection.cursor()
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        raise RuntimeError(f"User with ID {user_id} not deleted")


def count_admins(db_connection: Connection) -> int:
    query = (
        "SELECT COUNT(*)"
        "FROM users "
        "WHERE is_admin = TRUE"
    )
    cursor = db_connection.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    return row[0]


def set_admin(
    db_connection: Connection,
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
    cursor = db_connection.cursor()
    cursor.execute(query, values)
