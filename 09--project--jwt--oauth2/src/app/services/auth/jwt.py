import datetime
from datetime import timedelta

from jose import jwt
from jose.exceptions import JWTError

from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES


def get_subject(token: str) -> str | None:
    """Returns subject identifier from JWT access token."""

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        subject = payload.get("sub")
        if not subject:
            return None

    except JWTError:
        return None

    return subject


def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    """Creates a JWT access token."""
    src = data.copy()
    now = datetime.datetime.now(datetime.UTC)

    if not expires:
        expires = timedelta(minutes=JWT_EXPIRE_MINUTES)

    src.update({"exp": now + expires})
    jwt_encoded = jwt.encode(src, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return jwt_encoded
