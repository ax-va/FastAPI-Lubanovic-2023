from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm import Creature, Explorer
from app.models.schemas.creatures import CreatureResponse
from app.models.schemas.explorers import ExplorerRequest, ExplorerResponse
from app.repositories.errors import DuplicateBindingError as RepositoryDuplicateBindingError
from app.repositories.sqlalchemy import creatures as creatures_repository
from app.repositories.sqlalchemy import explorers as explorers_repository
from app.services.errors import DuplicateBindingError as ServiceDuplicateBindingError
from app.services.errors import NotFoundError

repository = explorers_repository


def to_response(explorer: Explorer) -> ExplorerResponse:
    return ExplorerResponse.model_validate(explorer, from_attributes=True)


def to_dict(explorer_request: ExplorerRequest) -> dict:
    return explorer_request.model_dump()


async def get_all(db_session: AsyncSession) -> list[ExplorerResponse]:
    return [to_response(creature) for creature in await repository.get_all(db_session)]


async def get_by_id(
    db_session: AsyncSession,
    explorer_id: int,
) -> ExplorerResponse | None:
    explorer = await repository.get_by_id(db_session, explorer_id)

    return to_response(explorer) if explorer is not None else None


async def create(
    db_session: AsyncSession,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    explorer = Explorer(**to_dict(explorer_request))

    try:
        created: Explorer = await repository.create(db_session, explorer)
        await db_session.commit()

    except Exception:
        await db_session.rollback()
        raise

    return to_response(created)


async def replace(
    db_session: AsyncSession,
    explorer_id: int,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    try:
        to_update: Explorer | None = await repository.get_by_id(db_session, explorer_id)
        if to_update is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        updated = await repository.replace(db_session, to_update, to_dict(explorer_request))
        await db_session.commit()

    except Exception:
        await db_session.rollback()
        raise

    return to_response(updated)


async def delete(
    db_session: AsyncSession,
    explorer_id: int,
) -> None:
    try:
        to_delete: Explorer | None = await repository.get_by_id(db_session, explorer_id)
        if to_delete is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        await repository.delete(db_session, to_delete)
        await db_session.commit()

    except Exception:
        await db_session.rollback()
        raise


async def bind(
    db_session: AsyncSession,
    explorer_id: int,
    creature_id: int,
) -> list[CreatureResponse]:
    from app.services.creatures import to_response as to_creature_response

    try:
        explorer: Explorer | None = await explorers_repository.get_by_id(db_session, explorer_id)
        if explorer is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        creature: Creature | None = await creatures_repository.get_by_id(db_session, creature_id)
        if creature is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        creatures: list[Creature] = await repository.bind(db_session, explorer, creature)
        await db_session.commit()

    except RepositoryDuplicateBindingError as e:
        await db_session.rollback()
        raise ServiceDuplicateBindingError(
            f"Explorer with ID {explorer_id} is already bound to creature with ID {creature_id}"
        ) from e

    except Exception:
        await db_session.rollback()
        raise

    return [to_creature_response(creature) for creature in creatures]


async def get_creatures(
    db_session: AsyncSession,
    explorer_id: int,
) -> list[CreatureResponse]:
    from app.services.creatures import to_response as to_creature_response

    explorer: Explorer | None = await repository.get_by_id(db_session, explorer_id)
    if explorer is None:
        raise NotFoundError(f"Explorer with ID {explorer_id} not found")

    creatures: list[Creature] = await repository.get_creatures(db_session, explorer)

    return [to_creature_response(creature) for creature in creatures]
