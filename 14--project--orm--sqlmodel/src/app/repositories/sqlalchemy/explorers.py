from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models.orm.explorer import Explorer
from app.models.orm.creature import Creature
from app.repositories.errors import DuplicateBindingError


def get_all(db_session: Session) -> list[Explorer]:
    statement = select(Explorer).order_by(Explorer.id)

    return list(db_session.exec(statement).all())


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


# SQLModel automatically maintains
# the many-to-many relationship between creatures and explorers.
def bind(
    db_session: Session,
    explorer: Explorer,
    creature: Creature,
) -> list[Creature]:
    explorer.creatures.append(creature)

    try:
        db_session.flush()

    except IntegrityError as e:
        raise DuplicateBindingError() from e

    return explorer.creatures
