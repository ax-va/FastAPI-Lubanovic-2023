from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.orm.explorer import Explorer
from app.models.orm.creature import Creature
from app.repositories.errors import DuplicateBindingError


async def get_all(db_session: AsyncSession) -> list[Explorer]:
    statement = select(Explorer).order_by(Explorer.id)
    result = await db_session.execute(statement)

    return list(result.scalars().all())


async def get_by_id(
    db_session: AsyncSession,
    explorer_id: int,
) -> Explorer | None:
    # noinspection PyTypeChecker
    return await db_session.get(Explorer, explorer_id)


async def create(
    db_session: AsyncSession,
    explorer: Explorer,
) -> Explorer:
    db_session.add(explorer)
    # Calling `flush` creates `id` for `explorer`
    await db_session.flush()

    return explorer


async def replace(
    db_session: AsyncSession,
    explorer: Explorer,
    field_to_value: dict[str, str | None]
) -> Explorer:

    for field, value in field_to_value.items():
        setattr(explorer, field, value)
    await db_session.flush()

    return explorer


async def delete(
    db_session: AsyncSession,
    explorer: Explorer,
) -> None:
    await db_session.delete(explorer)
    await db_session.flush()


# SQLModel automatically maintains
# the many-to-many relationship between creatures and explorers.
async def bind(
    db_session: AsyncSession,
    explorer: Explorer,
    creature: Creature,
) -> list[Creature]:

    # Rule:
    # In `AsyncSession`, always explicitly load a relationship
    # before using, modifying, or returning it.
    # Implicit lazy loading of relationships is error-prone;
    # use `refresh()` or `selectinload()`.
    # Scalar columns are normally already loaded
    # unless they have been explicitly expired or deferred.

    await db_session.refresh(
        explorer,
        attribute_names=["creatures"],
    )

    explorer.creatures.append(creature)

    try:
        await db_session.flush()

    except IntegrityError as e:
        raise DuplicateBindingError() from e

    return explorer.creatures


async def get_creatures(
    db_session: AsyncSession,
    explorer: Explorer,
) -> list[Creature]:

    # Rule:
    # In `AsyncSession`, always explicitly load a relationship
    # before using, modifying, or returning it.
    # Implicit lazy loading of relationships is error-prone;
    # use `refresh()` or `selectinload()`.
    # Scalar columns are normally already loaded
    # unless they have been explicitly expired or deferred.

    # noinspection PyTypeChecker
    statement = (
        select(Explorer)
        .options(selectinload(Explorer.creatures))
        .where(Explorer.id == explorer.id)
    )
    result = await db_session.execute(statement)
    explorer = result.scalar_one()

    return explorer.creatures
