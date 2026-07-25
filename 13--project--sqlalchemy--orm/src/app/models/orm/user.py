from sqlalchemy.orm import Mapped, mapped_column

from app.models.orm.base import Base


class User(Base):
    """SQLAlchemy ORM model for users table."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
