from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from app.models.orm.user import User
from ..errors import DuplicateError, INTEGRITY_ERROR_UNIQUE


async def get_all(db_session: AsyncSession) -> list[User]:
    statement = select(User).order_by(User.id)
    result = await db_session.execute(statement)

    return list(result.scalars().all())


async def get_by_id(
    db_session: AsyncSession,
    user_id: int,
) -> User | None:
    # noinspection PyTypeChecker
    return await db_session.get(User, user_id)


async def get_by_username(
    db_session: AsyncSession,
    username: str,
) -> User | None:
    statement = select(User).where(User.username == username)
    result = await db_session.execute(statement)

    return result.scalar_one()


async def create(
    db_session: AsyncSession,
    user: User,
) -> User:
    db_session.add(user)

    try:
        await db_session.flush()

    except IntegrityError as e:
        message = str(e.orig).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError() from e
        raise

    return user


async def replace(
    db_session: AsyncSession,
    user: User,
    field_to_value: dict[str, str | bool],
) -> User:
    for field, value in field_to_value.items():
        setattr(user, field, value)

    try:
        await db_session.flush()

    except IntegrityError as e:
        message = str(e.orig).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError() from e
        raise

    return user


async def count_admins(db_session: AsyncSession) -> int:
    statement = select(func.count(User.id)).where(User.is_admin)
    result = await db_session.execute(statement)

    return result.scalar_one()


async def soft_delete(
    db_session: AsyncSession,
    user: User,
) -> User:
    user.is_active = False
    await db_session.flush()

    return user


async def set_admin(
    db_session: AsyncSession,
    user: User,
    is_admin: bool,
) -> User:
    user.is_admin = is_admin
    await db_session.flush()

    return user
