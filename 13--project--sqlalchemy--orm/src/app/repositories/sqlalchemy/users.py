from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from app.models.orm.user import User
from ..errors import DuplicateError, INTEGRITY_ERROR_UNIQUE


def get_all(db_session: Session) -> Sequence[User]:
    statement = select(User).order_by(User.id)
    return db_session.scalars(statement).all()


def get_by_id(
    db_session: Session,
    user_id: int,
) -> User | None:
    # noinspection PyTypeChecker
    return db_session.get(User, user_id)


def get_by_username(
    db_session: Session,
    username: str,
) -> User | None:
    statement = select(User).where(User.username == username)

    return db_session.scalar(statement)


def create(
    db_session: Session,
    user: User,
) -> User:
    db_session.add(user)

    try:
        db_session.flush()

    except IntegrityError as e:
        message = str(e.orig).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError(f"Username {user.username!r} already exists") from e
        raise

    return user


def replace(
    db_session: Session,
    user: User,
    field_to_value: dict[str, str | bool],
) -> User:
    try:
        for field, value in field_to_value.items():
            setattr(user, field, value)
        db_session.flush()

    except IntegrityError as e:
        message = str(e.orig).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError(f"Username {user.username!r} already exists") from e
        raise

    return user


def count_admins(db_session: Session) -> int:
    statement = select(func.count(User.id)).where(User.is_admin)

    return db_session.scalar(statement) or 0


def delete(
    db_session: Session,
    user: User,
) -> User:
    user.is_active = False
    db_session.flush()

    return user


def set_admin(
    db_session: Session,
    user: User,
    is_admin: bool,
) -> User:
    user.is_admin = is_admin
    db_session.flush()

    return user
