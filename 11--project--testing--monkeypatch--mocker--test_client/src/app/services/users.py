from app.auth.jwt import decode_jwt_subject
from app.auth.passwords import hash_password, verify_password
from app.models.users import UserToCreate, UserToDB, UserFromDB, UserResponse, UserToReplace
from app.repositories.sqlite import users
from app.services.errors import LastAdminError, DoesNotExistError

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


def create(user: UserToCreate, is_admin: bool = False) -> UserResponse:
    user_to_db = UserToDB(
        username=user.username,
        password_hash=hash_password(user.password),
        is_active=True,
        is_admin=is_admin,
    )
    user_from_db: UserFromDB = repository.create(user_to_db)

    return to_response(user_from_db)


def replace(user_id: int, user: UserToReplace) -> UserResponse:
    response: UserResponse | None = get_by_id(user_id)

    if response is None:
        raise DoesNotExistError(f"User with ID {user_id} does not exist")

    user_to_db = UserToDB(
        username=user.username,
        password_hash=hash_password(user.password),
        is_active=user.is_active,
        is_admin=response.is_admin,
    )
    user_from_db: UserFromDB = repository.replace(user_id, user_to_db)

    return to_response(user_from_db)


def authenticate_user(username: str, password: str) -> UserFromDB | None:
    user = repository.get_by_username(username)

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    if not user.is_active:
        return None

    return user


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
    user = UserToCreate(username=username, password=password)
    return create(user, is_admin=True)


def ensure_admin_exists() -> None:
    if count_admins() > 0:
        return

    print("You must create an admin.")
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_admin(username, password)


def set_admin(user_id: int, is_admin: bool) -> UserResponse:
    response: UserResponse | None = get_by_id(user_id)

    if response is None:
        raise DoesNotExistError(f"User with ID {user_id} does not exist")

    if not is_admin and response.is_admin and count_admins() == 1:
        raise LastAdminError("Revoking the last admin is not allowed")

    updated: UserFromDB = repository.set_admin(user_id, is_admin)

    return to_response(updated)


def delete(user_id: int) -> bool:
    response: UserResponse | None = get_by_id(user_id)

    if response is None:
        return False

    if response.is_admin and count_admins() == 1:
        raise LastAdminError("Deleting the last admin is not allowed")

    return repository.delete(user_id)
