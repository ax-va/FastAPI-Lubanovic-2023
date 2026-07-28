from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from app.models.orm import Creature, Explorer, explorer_creature


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
    db_session.flush()


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
