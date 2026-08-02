from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.models.orm.explorer_creature import ExplorerCreature

# Import only for type checking to avoid circular imports.
# At runtime, the relationship target is resolved from the string annotation.
if TYPE_CHECKING:
    from app.models.orm.creature import Creature


class Explorer(SQLModel, table=True):
    """SQLModel for explorers table."""

    __tablename__ = 'explorers'

    id: int | None = Field(default=None, primary_key=True)
    name: str
    country: str | None = None
    description: str | None = None
    # The matching relationship on the opposite model `Creature` is `explorers`:
    # `Explorer.creatures` <-> `Creature.explorers`.
    # SQLModel keeps both sides of the relationship synchronized,
    # so changes made through one model are automatically reflected in the other.
    # If an `Creature` is added to this collection,
    # the corresponding `Explorer` is automatically added to the `Creature`'s `explorers` collection,
    # and vice versa.
    # Not a table column, but a lazily loading relationship.
    # SQLAlchemy loads it from the link table `ExplorerCreature` when accessed.
    creatures: list["Creature"] = Relationship(
        # `back_populates` specifies the name of
        # the matching relationship attribute on the opposite model.
        back_populates="explorers",
        link_model=ExplorerCreature,
    )
