from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.orm.explorer import Explorer
from app.models.orm.creature import Creature
from app.repositories.errors import DuplicateBindingError


async def get_all(db_session: AsyncSession) -> list[Creature]:
    statement = select(Creature).order_by(Creature.id)
    result = await db_session.execute(statement)

    return list(result.scalars().all())


async def get_by_id(
    db_session: AsyncSession,
    creature_id: int,
) -> Creature | None:
    # noinspection PyTypeChecker
    return await db_session.get(Creature, creature_id)


async def create(
    db_session: AsyncSession,
    creature: Creature,
) -> Creature:
    db_session.add(creature)
    # Calling `flush` creates `id` for `creature`
    await db_session.flush()

    return creature


async def replace(
    db_session: AsyncSession,
    creature: Creature,
    field_to_value: dict[str, str | None],
) -> Creature:

    for field, value in field_to_value.items():
        setattr(creature, field, value)
    await db_session.flush()

    return creature


async def delete(
    db_session: AsyncSession,
    creature: Creature,
) -> None:
    await db_session.delete(creature)
    await db_session.flush()


# SQLModel automatically maintains
# the many-to-many relationship between creatures and explorers.
async def bind(
    db_session: AsyncSession,
    creature: Creature,
    explorer: Explorer,
) -> list[Explorer]:
    creature.explorers.append(explorer)

    try:
        await db_session.flush()

    except IntegrityError as e:
        raise DuplicateBindingError() from e

    # Rule:
    # In `AsyncSession`, always explicitly load
    # a relationship before using or returning it.
    # Implicit lazy loading of relationships is
    # error-prone; use `refresh()` or `selectinload()`.
    # Scalar columns are normally already loaded
    # unless they have been explicitly expired or deferred.

    await db_session.refresh(
        creature,
        attribute_names=["explorers"],
    )

    return creature.explorers


async def get_explorers(
    db_session: AsyncSession,
    creature: Creature,
) -> list[Explorer]:

    # Rule:
    # In `AsyncSession`, always explicitly load
    # a relationship before using or returning it.
    # Implicit lazy loading of relationships is
    # error-prone; use `refresh()` or `selectinload()`.
    # Scalar columns are normally already loaded
    # unless they have been explicitly expired or deferred.

    # noinspection PyTypeChecker
    statement = (
        select(Creature)
        .options(selectinload(Creature.explorers))
        .where(Creature.id == creature.id)
    )
    result = await db_session.execute(statement)
    creature = result.scalar_one()

    return creature.explorers
