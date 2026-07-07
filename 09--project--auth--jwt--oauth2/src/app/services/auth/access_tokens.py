from datetime import timedelta

from app.services.auth import jwt


def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    return jwt.create_access_token(data=data, expires=expires)
