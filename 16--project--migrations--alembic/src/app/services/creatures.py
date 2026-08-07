from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm import Explorer
from app.models.orm.creature import Creature
from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.models.schemas.explorers import ExplorerResponse
from app.repositories.errors import DuplicateBindingError as RepositoryDuplicateBindingError
from app.repositories.sqlalchemy import creatures as creatures_repository
from app.repositories.sqlalchemy import explorers as explorers_repository
from app.services.errors import DuplicateBindingError as ServiceDuplicateBindingError
from app.services.errors import NotFoundError

repository = creatures_repository


def to_response(creature: Creature | Explorer) -> CreatureResponse:
    return CreatureResponse.model_validate(creature, from_attributes=True)


def to_dict(creature_request: CreatureRequest) -> dict:
    return creature_request.model_dump()


async def get_all(db_session: AsyncSession) -> list[CreatureResponse]:
    return [to_response(creature) for creature in await repository.get_all(db_session)]


async def get_by_id(
    db_session: AsyncSession,
    creature_id: int,
) -> CreatureResponse | None:
    creature = await repository.get_by_id(db_session, creature_id)

    return to_response(creature) if creature is not None else None


async def create(
    db_session: AsyncSession,
    creature_request: CreatureRequest,
) -> CreatureResponse:
    creature = Creature(**to_dict(creature_request))

    try:
        created: Creature = await repository.create(db_session, creature)
        await db_session.commit()

    except Exception:
        await db_session.rollback()
        raise

    return to_response(created)


async def replace(
    db_session: AsyncSession,
    creature_id: int,
    creature_request: CreatureRequest,
) -> CreatureResponse:
    try:
        to_update: Creature | None = await repository.get_by_id(db_session, creature_id)
        if to_update is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        updated = await repository.replace(db_session, to_update, to_dict(creature_request))
        await db_session.commit()

    except Exception:
        await db_session.rollback()
        raise

    return to_response(updated)


async def delete(
    db_session: AsyncSession,
    creature_id: int,
) -> None:
    try:
        to_delete: Creature | None = await repository.get_by_id(db_session, creature_id)
        if to_delete is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        await repository.delete(db_session, to_delete)
        await db_session.commit()

    except Exception:
        await db_session.rollback()
        raise


async def bind(
    db_session: AsyncSession,
    creature_id: int,
    explorer_id: int,
) -> list[ExplorerResponse]:
    from app.services.explorers import to_response as to_explorer_response

    try:
        creature: Creature | None = await creatures_repository.get_by_id(db_session, creature_id)
        if creature is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        explorer: Explorer | None = await explorers_repository.get_by_id(db_session, explorer_id)
        if explorer is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        explorers: list[Explorer] = await repository.bind(db_session, creature, explorer)
        await db_session.commit()

    except RepositoryDuplicateBindingError as e:
        await db_session.rollback()
        raise ServiceDuplicateBindingError(
            f"Creature with ID {creature_id} is already bound to explorer with ID {explorer_id}"
        ) from e

    except Exception:
        await db_session.rollback()
        raise

    return [to_explorer_response(explorer) for explorer in explorers]


async def get_explorers(
    db_session: AsyncSession,
    creature_id: int,
) -> list[ExplorerResponse]:
    from app.services.explorers import to_response as to_explorer_response

    creature: Creature | None = await repository.get_by_id(db_session, creature_id)
    if creature is None:
        raise NotFoundError(f"Creature with ID {creature_id} not found")

    explorers: list[Explorer] = await repository.get_explorers(db_session, creature)

    return [to_explorer_response(explorer) for explorer in explorers]
