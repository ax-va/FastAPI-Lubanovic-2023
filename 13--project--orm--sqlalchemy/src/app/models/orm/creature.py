from sqlalchemy.orm import Mapped, mapped_column

from app.models.orm.base import Base


class Creature(Base):
    """SQLAlchemy ORM model for creatures table."""

    __tablename__ = 'creatures'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    country: Mapped[str | None]
    # SQLAlchemy will automatically infer:
    # `country: Mapped[str | None] = mapped_column(nullable=True)`
    area: Mapped[str | None]
    description: Mapped[str | None]
    aka: Mapped[str | None]
