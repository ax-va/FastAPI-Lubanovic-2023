from sqlalchemy.orm.session import Session

from app.models.orm import Creature, Explorer
from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.models.schemas.explorers import ExplorerResponse
from app.repositories.errors import DuplicateBindingError as RepositoryDuplicateBindingError
from app.repositories.sqlalchemy import creatures as creatures_repository
from app.services.errors import DuplicateBindingError as ServiceDuplicateBindingError
from app.services.errors import NotFoundError

repository = creatures_repository


def to_response(creature: Creature) -> CreatureResponse:
    return CreatureResponse.model_validate(creature, from_attributes=True)


def to_dict(creature_request: CreatureRequest) -> dict:
    return creature_request.model_dump()


def get_all(db_session: Session) -> list[CreatureResponse]:
    return [to_response(creature) for creature in repository.get_all(db_session)]


def get_by_id(
    db_session: Session,
    creature_id: int,
) -> CreatureResponse | None:
    creature = repository.get_by_id(db_session, creature_id)

    return to_response(creature) if creature is not None else None


def create(
    db_session: Session,
    creature_request: CreatureRequest,
) -> CreatureResponse:
    creature = Creature(**to_dict(creature_request))

    try:
        created = repository.create(db_session, creature)
        db_session.commit()

    except Exception:
        db_session.rollback()
        raise

    return to_response(created)


def replace(
    db_session: Session,
    creature_id: int,
    creature_request: CreatureRequest,
) -> CreatureResponse:
    try:
        to_update: Creature | None = repository.get_by_id(db_session, creature_id)
        if to_update is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        updated = repository.replace(db_session, to_update, to_dict(creature_request))
        db_session.commit()

    except Exception:
        db_session.rollback()
        raise

    return to_response(updated)


def delete(
    db_session: Session,
    creature_id: int,
) -> None:
    try:
        to_delete: Creature | None = repository.get_by_id(db_session, creature_id)
        if to_delete is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        repository.delete(db_session, to_delete)
        db_session.commit()

    except Exception:
        db_session.rollback()
        raise


def bind(
    db_session: Session,
    creature_id: int,
    explorer_id: int,
) -> list[ExplorerResponse]:
    from app.repositories.sqlalchemy import explorers as explorers_repository
    from app.services.explorers import to_response as to_explorer_response

    try:
        creature: Creature | None = creatures_repository.get_by_id(db_session, creature_id)
        if creature is None:
            raise NotFoundError(f"Creature with ID {creature_id} not found")

        explorer: Explorer | None = explorers_repository.get_by_id(db_session, explorer_id)
        if explorer is None:
            raise NotFoundError(f"Explorer with ID {explorer_id} not found")

        repository.bind(db_session, creature, explorer)
        explorers: list[Explorer] = creatures_repository.get_explorers(db_session, creature)
        db_session.commit()

    except RepositoryDuplicateBindingError as e:
        db_session.rollback()
        raise ServiceDuplicateBindingError(
            f"Creature with ID {creature_id} is already bound to explorer with ID {explorer_id}"
        ) from e

    except Exception:
        db_session.rollback()
        raise

    return [to_explorer_response(explorer) for explorer in explorers]


def get_explorers(
    db_session: Session,
    creature_id: int,
) -> list[ExplorerResponse]:
    from app.services.explorers import to_response as to_explorer_response

    creature: Creature | None = creatures_repository.get_by_id(db_session, creature_id)
    if creature is None:
        raise NotFoundError(f"Creature with ID {creature_id} not found")

    explorers: list[Explorer] = repository.get_explorers(db_session, creature)

    return [to_explorer_response(explorer) for explorer in explorers]
