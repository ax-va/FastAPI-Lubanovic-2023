from sqlalchemy.orm.session import Session

from app.models.orm.creature import Creature
from app.models.schemas.creatures import CreatureRequest, CreatureResponse
from app.repositories.sqlalchemy import creatures as creatures_repository
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

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()

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

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()

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

    except Exception:
        db_session.rollback()
        raise

    db_session.commit()
