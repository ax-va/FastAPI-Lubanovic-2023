from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.orm.creature import Creature


def get_all(db_session: Session) -> list[Creature]:
    statement = select(Creature).order_by(Creature.id)

    return list(db_session.scalars(statement).all())


def get_by_id(
    db_session: Session,
    creature_id: int,
) -> Creature | None:
    # noinspection PyTypeChecker
    return db_session.get(Creature, creature_id)


def create(
    db_session: Session,
    creature: Creature,
) -> Creature:
    db_session.add(creature)
    # Calling `flush` creates `id` for `creature`
    db_session.flush()

    return creature


def replace(
    db_session: Session,
    creature: Creature,
    field_to_value: dict[str, str | None],
) -> Creature:

    for field, value in field_to_value.items():
        setattr(creature, field, value)
    db_session.flush()

    return creature


def delete(
    db_session: Session,
    creature: Creature,
) -> None:
    db_session.delete(creature)
    db_session.flush()
