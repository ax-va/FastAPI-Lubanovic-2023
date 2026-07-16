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


def get_all() -> list[UserResponse]:
    return [to_response(user) for user in repository.get_all()]


def get_by_id(user_id: int) -> UserResponse | None:
    user: UserFromDB | None = repository.get_by_id(user_id)

    if not user:
        return None

    return to_response(user)


def get_by_username(username: str) -> UserResponse | None:
    user: UserFromDB | None = repository.get_by_username(username)

    if not user:
        return None

    return to_response(user)


def create(user: UserToCreateRequest, is_admin: bool = False) -> UserResponse:
    to_create = UserToDB(
        username=user.username,
        password_hash=hash_password(user.password),
        is_active=True,
        is_admin=is_admin,
    )

    try:
        created_id = repository.create(to_create)

    except RepositoryDuplicateError as e:
        raise ServiceDuplicateError(str(e)) from e

    created: UserResponse | None = get_by_id(created_id)
    if created is None:
        raise RuntimeError(f"User with ID {created_id} could not be retrieved after creation")

    return created


def replace(user_id: int, user: UserToReplaceRequest) -> UserResponse:
    to_update: UserResponse | None = get_by_id(user_id)
    if to_update is None:
        raise NotFoundError(f"User with ID {user_id} not found")

    user_to_db = UserToDB(
        username=user.username,
        password_hash=hash_password(user.password),
        is_active=user.is_active,
        is_admin=to_update.is_admin,
    )

    try:
        repository.replace(user_id, user_to_db)

    except RepositoryDuplicateError as e:
        raise ServiceDuplicateError(str(e)) from e

    updated: UserResponse | None = get_by_id(user_id)
    if updated is None:
        raise RuntimeError(f"Updated user with ID {user_id} could not be retrieved after update")

    return updated


def verify_credentials(username: str, password: str) -> bool:
    user = repository.get_by_username(username)

    if user is None:
        return False

    if not verify_password(password, user.password_hash):
        return False

    if not user.is_active:
        return False

    return True


def get_by_token(token: str) -> UserResponse | None:
    subject = decode_jwt_subject(token)

    if subject is None:
        return None

    user = repository.get_by_username(subject)

    if user is None or not user.is_active:
        return None

    return to_response(user)


def count_admins() -> int:
    return repository.count_admins()


def create_admin(username: str, password: str) -> UserResponse:
    user = UserToCreateRequest(username=username, password=password)
    return create(user, is_admin=True)


def ensure_admin_exists() -> None:
    if count_admins() > 0:
        return

    print("You must create an admin.")
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_admin(username, password)


def delete(user_id: int) -> None:
    to_delete: UserResponse | None = get_by_id(user_id)
    if to_delete is None:
        raise NotFoundError(f"User with ID {user_id} not found")

    if to_delete.is_admin and count_admins() == 1:
        raise LastAdminError("Deleting the last admin is not allowed")

    repository.delete(user_id)


def set_admin(user_id: int, is_admin: bool) -> UserResponse:
    to_update: UserResponse | None = get_by_id(user_id)
    if to_update is None:
        raise NotFoundError(f"User with ID {user_id} not found")

    if not is_admin and to_update.is_admin and count_admins() == 1:
        raise LastAdminError("Revoking the last admin is not allowed")

    repository.set_admin(user_id, is_admin)

    updated: UserResponse | None = get_by_id(user_id)
    if updated is None:
        raise RuntimeError(f"Updated user with ID {user_id} could not be retrieved after update")

    return updated
