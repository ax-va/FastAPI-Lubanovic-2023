from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models.orm.explorer import Explorer
from app.models.orm.creature import Creature
from app.repositories.errors import DuplicateBindingError


def get_all(db_session: Session) -> list[Creature]:
    statement = select(Creature).order_by(Creature.id)

    return list(db_session.exec(statement).all())


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


# SQLModel automatically maintains
# the many-to-many relationship between creatures and explorers.
def bind(
    db_session: Session,
    creature: Creature,
    explorer: Explorer,
) -> list[Explorer]:
    creature.explorers.append(explorer)

    try:
        db_session.flush()

    except IntegrityError as e:
        raise DuplicateBindingError(
            f"Creature with ID {creature.id} is already bound to explorer with ID {explorer.id}"
        ) from e

    return creature.explorers
