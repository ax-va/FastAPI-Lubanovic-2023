from sqlalchemy import Column, ForeignKey, Table

from .base import Base

# many-to-many relationship between explorers and creatures
explorer_creature = Table(
    'explorer_creature_relationship',
    Base.metadata,
    Column(
        "explorer_id",
        ForeignKey("explorers.id"),
        primary_key=True,
    ),
    Column(
        "creature_id",
        ForeignKey("creatures.id"),
        primary_key=True,
    )
)
