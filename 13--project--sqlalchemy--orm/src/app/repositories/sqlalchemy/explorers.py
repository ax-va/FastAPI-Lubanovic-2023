from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.orm import Creature, Explorer, explorer_creature
from app.repositories.errors import DuplicateBindingError


def get_all(db_session: Session) -> list[Explorer]:
    statement = select(Explorer).order_by(Explorer.id)

    return list(db_session.scalars(statement).all())


def get_by_id(
    db_session: Session,
    explorer_id: int,
) -> Explorer | None:
    # noinspection PyTypeChecker
    return db_session.get(Explorer, explorer_id)


def create(
    db_session: Session,
    explorer: Explorer,
) -> Explorer:
    db_session.add(explorer)
    # Calling `flush` creates `id` for `explorer`
    db_session.flush()

    return explorer


def replace(
    db_session: Session,
    explorer: Explorer,
    field_to_value: dict[str, str | None]
) -> Explorer:

    for field, value in field_to_value.items():
        setattr(explorer, field, value)
    db_session.flush()

    return explorer


def delete(
    db_session: Session,
    explorer: Explorer,
) -> None:
    db_session.delete(explorer)
    db_session.flush()


def bind(
    db_session: Session,
    explorer: Explorer,
    creature: Creature,
) -> None:
    statement = insert(explorer_creature).values(
        explorer_id=explorer.id,
        creature_id=creature.id,
    )
    db_session.execute(statement)

    try:
        db_session.flush()

    except IntegrityError as e:
        raise DuplicateBindingError(
            f"Explorer with ID {explorer.id} is already bound to creature with ID {creature.id}"
        ) from e


def get_creatures(
    db_session: Session,
    explorer: Explorer,
) -> list[Creature]:
    statement = (
        select(Creature).join(
            explorer_creature,
            Creature.id == explorer_creature.c.creature_id,
        ).where(
            explorer_creature.c.explorer_id == explorer.id,
        ).order_by(Creature.id)
    )

    return list(db_session.scalars(statement).all())
