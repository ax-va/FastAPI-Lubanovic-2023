from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.models.orm.explorer_creature import ExplorerCreature

# Import only for type checking to avoid circular imports.
# At runtime, the relationship target is resolved from the string annotation.
if TYPE_CHECKING:
    from app.models.orm.explorer import Explorer


class Creature(SQLModel, table=True):
    """SQLModel for creatures table."""

    __tablename__ = 'creatures'

    id: int | None = Field(default=None, primary_key=True)
    name: str
    country: str | None = None
    area: str | None = None
    description: str | None = None
    aka: str | None = None
    # The matching relationship on the opposite model `Explorer` is `creatures`:
    # `Creature.explorers` <-> `Explorer.creatures`.
    # SQLModel keeps both sides of the relationship synchronized,
    # so changes made through one model are automatically reflected in the other.
    # If an `Explorer` is added to this collection,
    # the corresponding `Creature` is automatically added to the `Explorer`'s `creatures` collection,
    # and vice versa.
    explorers: list["Explorer"] = Relationship(
        # `back_populates` specifies the name of
        # the matching relationship attribute on the opposite model.
        back_populates="creatures",
        link_model=ExplorerCreature,
    )
