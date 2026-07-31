from typing import cast

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, func, select

from app.models.orm.user import User
from ..errors import DuplicateError, INTEGRITY_ERROR_UNIQUE


def get_all(db_session: Session) -> list[User]:
    statement = select(User).order_by(User.id)
    return list(db_session.scalars(statement).all())


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
            raise DuplicateError() from e
        raise

    return user


def replace(
    db_session: Session,
    user: User,
    field_to_value: dict[str, str | bool],
) -> User:
    for field, value in field_to_value.items():
        setattr(user, field, value)

    try:
        db_session.flush()

    except IntegrityError as e:
        message = str(e.orig).lower()
        if INTEGRITY_ERROR_UNIQUE in message:
            raise DuplicateError() from e
        raise

    return user


def count_admins(db_session: Session) -> int:
    statement = select(func.count(User.id)).where(User.is_admin)

    # SQLAlchemy cannot infer that `COUNT()` always returns an `int`
    return cast(int, db_session.exec(statement).one())


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
