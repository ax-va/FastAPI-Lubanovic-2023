from app.models.users import UserToCreate, UserToDB, UserFromDB, UserResponse
from app.repositories.sqlite import users
from app.services.auth.jwt import decode_jwt_subject
from app.services.auth.passwords import hash_password, verify_password

repository = users


def to_response(user: UserFromDB) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        is_active=user.is_active,
    )


def to_db(user: UserToCreate) -> UserToDB:
    return UserToDB(
        username=user.username,
        password_hash=hash_password(user.password),
        is_active=True,
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


def create(user: UserToCreate) -> UserResponse:
    user_from_db: UserFromDB = repository.create(to_db(user))
    return to_response(user_from_db)


def replace(user_id: int, user: UserToDB) -> UserResponse:
    user_from_db: UserFromDB = repository.replace(user_id, user)
    return to_response(user_from_db)


def delete(user_id: int) -> bool:
    return repository.delete(user_id)


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
