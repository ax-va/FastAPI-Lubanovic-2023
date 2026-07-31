from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.orm import Creature, Explorer, explorer_creature
from app.repositories.errors import DuplicateBindingError


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


def bind(
    db_session: Session,
    creature: Creature,
    explorer: Explorer,

) -> None:
    statement = insert(explorer_creature).values(
        creature_id=creature.id,
        explorer_id=explorer.id,
    )
    db_session.execute(statement)

    try:
        db_session.flush()

    except IntegrityError as e:
        raise DuplicateBindingError() from e


def get_explorers(
    db_session: Session,
    creature: Creature,
) -> list[Explorer]:
    statement = (
        select(Explorer).join(
            explorer_creature,
            Explorer.id == explorer_creature.c.explorer_id,
        ).where(
            explorer_creature.c.creature_id == creature.id,
        ).order_by(Explorer.id)
    )

    return list(db_session.scalars(statement).all())