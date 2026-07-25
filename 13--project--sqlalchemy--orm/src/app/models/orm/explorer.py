from sqlalchemy.orm import Mapped, mapped_column

from app.models.orm.base import Base


class Explorer(Base):
    """SQLAlchemy ORM model for explorers table."""

    __tablename__ = 'explorers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    country: Mapped[str | None]
    description: Mapped[str | None]
