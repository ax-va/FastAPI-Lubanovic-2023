from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.orm.explorer import Explorer


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
    # Calling `flush` creates `id` for `creature`
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
