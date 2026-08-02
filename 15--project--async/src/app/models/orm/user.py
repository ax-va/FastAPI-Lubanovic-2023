from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """SQLModel for users table."""

    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password_hash: str
    is_active: bool = True
    is_admin: bool = False
