from sqlalchemy.orm.session import Session

from app.models.orm.creature import Creature
from app.models.orm.explorer import Explorer
from app.models.schemas.creatures import CreatureResponse
from app.models.schemas.explorers import ExplorerResponse
from app.repositories.sqlalchemy import creatures as creatures_repository
from app.repositories.sqlalchemy import explorer_creature as explorer_creature_repository
from app.repositories.sqlalchemy import explorers as explorers_repository
from app.services.creatures import to_response as to_creature_response
from app.services.explorers import to_response as to_explorer_response
from app.services.errors import NotFoundError

repository = explorer_creature_repository


def bind(
    db_session: Session,
    explorer_id: int,
    creature_id: int,
) -> None:
    try:

        explorer: Explorer | None = explorers_repository.get_by_id(db_session, explorer_id)
        if explorer is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        creature: Creature | None = creatures_repository.get_by_id(db_session, creature_id)
        if creature is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        repository.bind(db_session, explorer, creature)

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()


def get_creatures(
    db_session: Session,
    explorer_id: int,
) -> list[CreatureResponse]:
    try:

        explorer: Explorer | None = explorers_repository.get_by_id(db_session, explorer_id)
        if explorer is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        creatures: list[Creature] = repository.get_creatures(db_session, explorer)

    except Exception:
        db_session.rollback()
        raise

    return [to_creature_response(creature) for creature in creatures]


def get_explorers(
    db_session: Session,
    creature_id: int,
) -> list[ExplorerResponse]:
    try:

        creature: Creature | None = creatures_repository.get_by_id(db_session, creature_id)
        if creature is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        explorers: list[Explorer] = repository.get_explorers(db_session, creature)

    except Exception:
        db_session.rollback()
        raise

    return [to_explorer_response(explorer) for explorer in explorers]
