from app.models.users import UserToCreate, UserToDB, UserFromDB, UserResponse
from app.repositories.sqlite import users
from app.services.auth.passwords import hash_password

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


def create(user: UserToCreate) -> UserFromDB:
    return repository.create(to_db(user))


def replace(user_id: int, user: UserToDB) -> UserFromDB:
    return repository.replace(user_id, user)


def delete(user_id: int) -> bool:
    return repository.delete(user_id)
