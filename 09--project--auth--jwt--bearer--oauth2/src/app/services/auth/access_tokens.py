from datetime import timedelta

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.auth import jwt


def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    if not expires:
        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return jwt.encode_jwt(data=data, expires=expires)
