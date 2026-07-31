from sqlite3 import Connection

from app.auth.jwt import decode_jwt_subject
from app.auth.passwords import hash_password, verify_password
from app.models.schemas.users import UserToCreateRequest, UserToRepo, UserFromRepo, UserResponse, UserToReplaceRequest
from app.repositories.errors import DuplicateError as RepositoryDuplicateError
from app.repositories.sqlite import users as users_repository
from app.services.errors import LastAdminError, NotFoundError
from app.services.errors import DuplicateError as ServiceDuplicateError

repository = users_repository


def to_response(user_from_repo: UserFromRepo) -> UserResponse:
    return UserResponse(
        id=user_from_repo.id,
        username=user_from_repo.username,
        is_active=user_from_repo.is_active,
        is_admin=user_from_repo.is_admin,
    )


def get_all(db_connection: Connection) -> list[UserResponse]:
    return [to_response(user) for user in repository.get_all(db_connection)]


def get_by_id(
    db_connection: Connection,
    user_id: int,
) -> UserResponse | None:
    user_from_repo: UserFromRepo | None = repository.get_by_id(db_connection, user_id)

    if not user_from_repo:
        return None

    return to_response(user_from_repo)


def get_by_username(
    db_connection: Connection,
    username: str,
) -> UserResponse | None:
    user_from_repo: UserFromRepo | None = repository.get_by_username(db_connection, username)

    if not user_from_repo:
        return None

    return to_response(user_from_repo)


def create(
    db_connection: Connection,
    user_request: UserToCreateRequest,
    is_admin: bool = False,
) -> UserResponse:
    try:
        to_create = UserToRepo(
            username=user_request.username,
            password_hash=hash_password(user_request.password),
            is_active=True,
            is_admin=is_admin,
        )

        created_id = repository.create(db_connection, to_create)

        created: UserResponse | None = get_by_id(db_connection, created_id)
        if created is None:
            raise RuntimeError(f"User with ID {created_id} could not be retrieved after creation")

        db_connection.commit()

    except RepositoryDuplicateError as e:
        db_connection.rollback()
        raise ServiceDuplicateError(str(e)) from e

    except Exception:
        db_connection.rollback()
        raise

    return created


def replace(
    db_connection: Connection,
    user_id: int,
    user_request: UserToReplaceRequest,
) -> UserResponse:
    try:
        to_update: UserResponse | None = get_by_id(db_connection, user_id)
        if to_update is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        user_to_repo = UserToRepo(
            username=user_request.username,
            password_hash=hash_password(user_request.password),
            is_active=user_request.is_active,
            is_admin=to_update.is_admin,
        )

        repository.replace(db_connection, user_id, user_to_repo)

        updated: UserResponse | None = get_by_id(db_connection, user_id)
        if updated is None:
            raise RuntimeError(f"Updated user with ID {user_id} could not be retrieved after update")

        db_connection.commit()

    except RepositoryDuplicateError as e:
        db_connection.rollback()
        raise ServiceDuplicateError(str(e)) from e

    except Exception:
        db_connection.rollback()
        raise

    return updated


def verify_credentials(
    db_connection: Connection,
    username: str,
    password: str,
) -> bool:
    user_from_repo = repository.get_by_username(db_connection, username)

    if user_from_repo is None:
        return False

    if not verify_password(password, user_from_repo.password_hash):
        return False

    if not user_from_repo.is_active:
        return False

    return True


def get_by_token(
    db_connection: Connection,
    token: str,
) -> UserResponse | None:
    subject = decode_jwt_subject(token)

    if subject is None:
        return None

    user_response = get_by_username(db_connection, subject)

    if user_response is None or not user_response.is_active:
        return None

    return to_response(user_response)


def count_admins(db_connection: Connection) -> int:
    return repository.count_admins(db_connection)


def create_admin(
    db_connection: Connection,
    username: str,
    password: str,
) -> UserResponse:
    user_request = UserToCreateRequest(username=username, password=password)
    return create(db_connection, user_request, is_admin=True)


def ensure_admin_exists(db_connection: Connection) -> None:
    if count_admins(db_connection) > 0:
        return

    print("You must create an admin.")
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_admin(db_connection, username, password)


def delete(
    db_connection: Connection,
    user_id: int,
) -> None:
    try:
        to_delete: UserResponse | None = get_by_id(db_connection, user_id)
        if to_delete is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        if to_delete.is_admin and count_admins(db_connection) == 1:
            raise LastAdminError("Deleting the last admin is not allowed")

        repository.delete(db_connection, user_id)
        db_connection.commit()

    except Exception:
        db_connection.rollback()
        raise


def set_admin(
    db_connection: Connection,
    user_id: int,
    is_admin: bool,
) -> UserResponse:
    try:
        to_update: UserResponse | None = get_by_id(db_connection, user_id)
        if to_update is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        if not is_admin and to_update.is_admin and count_admins(db_connection) == 1:
            raise LastAdminError("Revoking the last admin is not allowed")

        repository.set_admin(db_connection, user_id, is_admin)

        updated: UserResponse | None = get_by_id(db_connection, user_id)
        if updated is None:
            raise RuntimeError(f"Updated user with ID {user_id} could not be retrieved after update")

        db_connection.commit()

    except Exception:
        db_connection.rollback()
        raise

    return updated
