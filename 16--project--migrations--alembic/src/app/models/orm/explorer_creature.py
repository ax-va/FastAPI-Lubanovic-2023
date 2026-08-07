from sqlmodel import Field, SQLModel



class ExplorerCreature(SQLModel, table=True):
    """Many-to-many relationship between explorers and creatures."""

    __tablename__ = "explorer_creature_relationship"

    explorer_id: int = Field(
        foreign_key="explorers.id",
        primary_key=True,
    )
    creature_id: int = Field(
        foreign_key="creatures.id",
        primary_key=True,
    )
