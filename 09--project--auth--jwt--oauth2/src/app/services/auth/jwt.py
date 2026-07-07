import datetime
from datetime import timedelta

from jose import jwt
from jose.exceptions import JWTError

from app.config import JWT_SECRET_KEY, JWT_ALGORITHM


def decode_jwt_subject(token: str) -> str | None:
    """Returns subject identifier from JWT access token."""

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        subject = payload.get("sub")
        if not subject:
            return None

    except JWTError:
        return None

    return subject


def encode_jwt(data: dict, expires: timedelta) -> str:
    """Creates a JWT access token."""
    src = data.copy()
    now = datetime.datetime.now(datetime.UTC)
    src["exp"] = now + expires
    jwt_encoded = jwt.encode(src, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return jwt_encoded
