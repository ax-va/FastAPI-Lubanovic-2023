from sqlalchemy.ext.asyncio import AsyncSession

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


async def get_all(db_session: AsyncSession) -> list[UserResponse]:
    return [to_response(user) for user in await repository.get_all(db_session)]


async def get_by_id(
    db_session: AsyncSession,
    user_id: int,
) -> UserResponse | None:
    user: User | None = await repository.get_by_id(db_session, user_id)

    return to_response(user) if user is not None else None


async def get_by_username(
    db_session: AsyncSession,
    username: str,
) -> UserResponse | None:
    user: User | None = await repository.get_by_username(db_session, username)

    return to_response(user) if user is not None else None


async def create(
    db_session: AsyncSession,
    user_request: UserToCreateRequest,
    is_admin: bool = False,
) -> UserResponse:
    user = User(
        username=user_request.username,
        password_hash=hash_password(user_request.password),
        is_admin=is_admin,
    )

    try:
        created: User = await repository.create(db_session, user)
        await db_session.commit()

    except RepositoryDuplicateError as e:
        await db_session.rollback()
        raise ServiceDuplicateError(
            f"Username {user_request.username!r} already exists"
        ) from e

    except Exception:
        await db_session.rollback()
        raise

    return to_response(created)


async def replace(
    db_session: AsyncSession,
    user_id: int,
    user_request: UserToReplaceRequest,
) -> UserResponse:
    try:
        to_update: User | None = await repository.get_by_id(db_session, user_id)
        if to_update is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        updated: User = await repository.replace(db_session, to_update, to_dict(user_request))
        await db_session.commit()

    except RepositoryDuplicateError as e:
        await db_session.rollback()
        raise ServiceDuplicateError(
            f"Username {user_request.username!r} already exists"
        ) from e

    except Exception:
        await db_session.rollback()
        raise

    return to_response(updated)


async def verify_credentials(
    db_session: AsyncSession,
    username: str,
    password: str,
) -> bool:
    user: User | None = await repository.get_by_username(db_session, username)

    if user is None:
        return False

    if not verify_password(password, user.password_hash):
        return False

    if not user.is_active:
        return False

    return True


async def get_by_token(
    db_session: AsyncSession,
    token: str,
) -> UserResponse | None:
    subject = decode_jwt_subject(token)

    if subject is None:
        return None

    user: User | None = await repository.get_by_username(db_session, subject)

    if user is None or not user.is_active:
        return None

    return to_response(user)


async def count_admins(db_session: AsyncSession) -> int:
    return await repository.count_admins(db_session)


async def create_admin(
    db_session: AsyncSession,
    username: str,
    password: str,
) -> UserResponse:
    user_request = UserToCreateRequest(username=username, password=password)

    return await create(db_session, user_request, is_admin=True)


async def ensure_admin_exists(db_session: AsyncSession) -> None:
    if await count_admins(db_session) > 0:
        return

    print("You must create an admin.")
    username = input("Enter username: ")
    password = input("Enter password: ")
    await create_admin(db_session, username, password)


async def soft_delete(
    db_session: AsyncSession,
    user_id: int,
) -> UserResponse:
    try:
        to_delete: User | None = await repository.get_by_id(db_session, user_id)
        if to_delete is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        if (
            to_delete.is_admin
            and await count_admins(db_session) == 1
        ):
            raise LastAdminError("Deleting the last admin is not allowed")

        soft_deleted: User = await repository.soft_delete(db_session, to_delete)
        await db_session.commit()

    except Exception:
        await db_session.rollback()
        raise

    return to_response(soft_deleted)


async def set_admin(
    db_session: AsyncSession,
    user_id: int,
    is_admin: bool,
) -> UserResponse:
    try:
        to_update: User | None = await repository.get_by_id(db_session, user_id)
        if to_update is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        if (
            not is_admin
            and to_update.is_admin
            and await count_admins(db_session) == 1
        ):
            raise LastAdminError("Revoking the last admin is not allowed")

        updated: User = await repository.set_admin(db_session, to_update, is_admin)
        await db_session.commit()

    except Exception:
        await db_session.rollback()
        raise

    return to_response(updated)
