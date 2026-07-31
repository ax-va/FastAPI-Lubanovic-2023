from sqlalchemy.orm.session import Session

from app.auth.jwt import decode_jwt_subject
from app.auth.passwords import verify_password, password_hash, hash_password
from app.models.orm.user import User
from app.models.schemas.users import UserToCreateRequest, UserToReplaceRequest, UserResponse
from app.repositories.errors import DuplicateError as RepositoryDuplicateError
from app.repositories.sqlalchemy import users as users_repository
from app.services.errors import LastAdminError, NotFoundError
from app.services.errors import DuplicateError as ServiceDuplicateError

repository = users_repository


def to_response(user: User) -> UserResponse:
    return UserResponse.model_validate(user, from_attributes=True)


def to_dict(user_request: UserToCreateRequest | UserToReplaceRequest) -> dict:
    return user_request.model_dump()


def get_all(db_session: Session) -> list[UserResponse]:
    return [to_response(user) for user in repository.get_all(db_session)]


def get_by_id(
    db_session: Session,
    user_id: int,
) -> UserResponse | None:
    user: User | None = repository.get_by_id(db_session, user_id)

    return to_response(user) if user is not None else None


def get_by_username(
    db_session: Session,
    username: str,
) -> UserResponse | None:
    user: User | None = repository.get_by_username(db_session, username)

    return to_response(user) if user is not None else None


def create(
    db_session: Session,
    user_request: UserToCreateRequest,
    is_admin: bool = False,
) -> UserResponse:
    user = User(
        username=user_request.username,
        password_hash=hash_password(user_request.password),
        is_admin=is_admin,
    )

    try:
        created = repository.create(db_session, user)

    except RepositoryDuplicateError as e:
        db_session.rollback()
        raise ServiceDuplicateError(
            f"Username {user_request.username!r} already exists"
        ) from e

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()

    return to_response(created)


def replace(
    db_session: Session,
    user_id: int,
    user_request: UserToReplaceRequest,
) -> UserResponse:
    try:
        to_update: User | None = repository.get_by_id(db_session, user_id)
        if to_update is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        updated = repository.replace(db_session, to_update, to_dict(user_request))

    except RepositoryDuplicateError as e:
        db_session.rollback()
        raise ServiceDuplicateError(
            f"Username {user_request.username!r} already exists"
        ) from e

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()

    return to_response(updated)


def verify_credentials(
    db_session: Session,
    username: str,
    password: str,
) -> bool:
    user = repository.get_by_username(db_session, username)

    if user is None:
        return False

    if not verify_password(password, user.password_hash):
        return False

    if not user.is_active:
        return False

    return True


def get_by_token(
    db_session: Session,
    token: str,
) -> UserResponse | None:
    subject = decode_jwt_subject(token)

    if subject is None:
        return None

    user = repository.get_by_username(db_session, subject)

    if user is None or not user.is_active:
        return None

    return to_response(user)


def count_admins(db_session: Session) -> int:
    return repository.count_admins(db_session)


def create_admin(
    db_session: Session,
    username: str,
    password: str,
) -> UserResponse:
    user_request = UserToCreateRequest(username=username, password=password)

    return create(db_session, user_request, is_admin=True)


def ensure_admin_exists(db_session: Session) -> None:
    if count_admins(db_session) > 0:
        return

    print("You must create an admin.")
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_admin(db_session, username, password)


def delete(
    db_session: Session,
    user_id: int,
) -> UserResponse:
    try:
        to_delete: User | None = repository.get_by_id(db_session, user_id)
        if to_delete is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        if to_delete.is_admin and count_admins(db_session) == 1:
            raise LastAdminError("Deleting the last admin is not allowed")

        deleted = repository.delete(db_session, to_delete)

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()

    return to_response(deleted)


def set_admin(
    db_session: Session,
    user_id: int,
    is_admin: bool,
) -> UserResponse:
    try:
        to_update: User | None = repository.get_by_id(db_session, user_id)
        if to_update is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        if not is_admin and to_update.is_admin and count_admins(db_session) == 1:
            raise LastAdminError("Revoking the last admin is not allowed")

        updated = repository.set_admin(db_session, to_update, is_admin)

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()

    return to_response(updated)
