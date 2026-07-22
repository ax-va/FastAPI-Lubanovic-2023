from sqlite3 import Connection

from app.auth.jwt import decode_jwt_subject
from app.auth.passwords import hash_password, verify_password
from app.models.users import UserToCreateRequest, UserToDB, UserFromDB, UserResponse, UserToReplaceRequest
from app.repositories.errors import DuplicateError as RepositoryDuplicateError
from app.repositories.sqlite import users as users
from app.services.errors import LastAdminError, NotFoundError
from app.services.errors import DuplicateError as ServiceDuplicateError

repository = users


def to_response(user: UserFromDB) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
        is_admin=user.is_admin,
    )


def get_all(connection: Connection) -> list[UserResponse]:
    return [to_response(user) for user in repository.get_all(connection)]


def get_by_id(
    connection: Connection,
    user_id: int,
) -> UserResponse | None:
    user: UserFromDB | None = repository.get_by_id(connection, user_id)

    if not user:
        return None

    return to_response(user)


def get_by_username(
    connection: Connection,
    username: str,
) -> UserResponse | None:
    user: UserFromDB | None = repository.get_by_username(connection, username)

    if not user:
        return None

    return to_response(user)


def create(
    connection: Connection,
    user: UserToCreateRequest,
    is_admin: bool = False,
) -> UserResponse:
    try:
        to_create = UserToDB(
            username=user.username,
            password_hash=hash_password(user.password),
            is_active=True,
            is_admin=is_admin,
        )

        created_id = repository.create(connection, to_create)

        created: UserResponse | None = get_by_id(connection, created_id)
        if created is None:
            raise RuntimeError(f"User with ID {created_id} could not be retrieved after creation")

    except RepositoryDuplicateError as e:
        connection.rollback()
        raise ServiceDuplicateError(str(e)) from e

    except Exception:
        connection.rollback()
        raise

    connection.commit()

    return created


def replace(
    connection: Connection,
    user_id: int,
    user: UserToReplaceRequest,
) -> UserResponse:
    try:
        to_update: UserResponse | None = get_by_id(connection, user_id)
        if to_update is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        user_to_db = UserToDB(
            username=user.username,
            password_hash=hash_password(user.password),
            is_active=user.is_active,
            is_admin=to_update.is_admin,
        )

        repository.replace(connection, user_id, user_to_db)

        updated: UserResponse | None = get_by_id(connection, user_id)
        if updated is None:
            raise RuntimeError(f"Updated user with ID {user_id} could not be retrieved after update")

    except RepositoryDuplicateError as e:
        connection.rollback()
        raise ServiceDuplicateError(str(e)) from e

    except Exception:
        connection.rollback()
        raise

    connection.commit()

    return updated


def verify_credentials(
    connection: Connection,
    username: str,
    password: str,
) -> bool:
    user = repository.get_by_username(connection, username)

    if user is None:
        return False

    if not verify_password(password, user.password_hash):
        return False

    if not user.is_active:
        return False

    return True


def get_by_token(
    connection: Connection,
    token: str,
) -> UserResponse | None:
    subject = decode_jwt_subject(token)

    if subject is None:
        return None

    user = repository.get_by_username(connection, subject)

    if user is None or not user.is_active:
        return None

    return to_response(user)


def count_admins(connection: Connection) -> int:
    return repository.count_admins(connection)


def create_admin(
    connection: Connection,
    username: str,
    password: str,
) -> UserResponse:
    user = UserToCreateRequest(username=username, password=password)
    return create(connection, user, is_admin=True)


def ensure_admin_exists(connection: Connection) -> None:
    if count_admins(connection) > 0:
        return

    print("You must create an admin.")
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_admin(connection, username, password)


def delete(
    connection: Connection,
    user_id: int,
) -> None:
    try:
        to_delete: UserResponse | None = get_by_id(connection, user_id)
        if to_delete is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        if to_delete.is_admin and count_admins(connection) == 1:
            raise LastAdminError("Deleting the last admin is not allowed")

        repository.delete(connection, user_id)

    except Exception:
        connection.rollback()
        raise

    connection.commit()


def set_admin(
    connection: Connection,
    user_id: int,
    is_admin: bool,
) -> UserResponse:
    try:
        to_update: UserResponse | None = get_by_id(connection, user_id)
        if to_update is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        if not is_admin and to_update.is_admin and count_admins(connection) == 1:
            raise LastAdminError("Revoking the last admin is not allowed")

        repository.set_admin(connection, user_id, is_admin)

        updated: UserResponse | None = get_by_id(connection, user_id)
        if updated is None:
            raise RuntimeError(f"Updated user with ID {user_id} could not be retrieved after update")

    except Exception:
        connection.rollback()
        raise

    connection.commit()

    return updated
