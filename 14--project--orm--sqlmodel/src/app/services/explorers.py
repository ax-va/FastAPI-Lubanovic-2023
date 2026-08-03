from sqlalchemy.orm.session import Session

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


def get_all(db_session: Session) -> list[ExplorerResponse]:
    return [to_response(creature) for creature in repository.get_all(db_session)]


def get_by_id(
    db_session: Session,
    explorer_id: int,
) -> ExplorerResponse | None:
    explorer = repository.get_by_id(db_session, explorer_id)

    return to_response(explorer) if explorer is not None else None


def create(
    db_session: Session,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    explorer = Explorer(**to_dict(explorer_request))

    try:
        created: Explorer = repository.create(db_session, explorer)
        db_session.commit()

    except Exception:
        db_session.rollback()
        raise

    return to_response(created)


def replace(
    db_session: Session,
    explorer_id: int,
    explorer_request: ExplorerRequest,
) -> ExplorerResponse:
    try:
        to_update: Explorer | None = repository.get_by_id(db_session, explorer_id)
        if to_update is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        updated = repository.replace(db_session, to_update, to_dict(explorer_request))
        db_session.commit()

    except Exception:
        db_session.rollback()
        raise

    return to_response(updated)


def delete(
    db_session: Session,
    explorer_id: int,
) -> None:
    try:
        to_delete: Explorer | None = repository.get_by_id(db_session, explorer_id)
        if to_delete is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        repository.delete(db_session, to_delete)
        db_session.commit()

    except Exception:
        db_session.rollback()
        raise


def bind(
    db_session: Session,
    explorer_id: int,
    creature_id: int,
) -> list[CreatureResponse]:
    from app.services.creatures import to_response as to_creature_response

    try:
        explorer: Explorer | None = explorers_repository.get_by_id(db_session, explorer_id)
        if explorer is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        creature: Creature | None = creatures_repository.get_by_id(db_session, creature_id)
        if creature is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        repository.bind(db_session, explorer, creature)
        db_session.commit()

    except RepositoryDuplicateBindingError as e:
        db_session.rollback()
        raise ServiceDuplicateBindingError(
            f"Explorer with ID {explorer_id} is already bound to creature with ID {creature_id}"
        ) from e

    except Exception:
        db_session.rollback()
        raise

    return [to_creature_response(creature) for creature in explorer.creatures]


def get_creatures(
    db_session: Session,
    explorer_id: int,
) -> list[CreatureResponse]:
    from app.services.creatures import to_response as to_creature_response

    explorer: Explorer | None = repository.get_by_id(db_session, explorer_id)
    if explorer is None:
        raise NotFoundError(f"Explorer with ID {explorer_id} not found")

    return [to_creature_response(creature) for creature in explorer.creatures]
