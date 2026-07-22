from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.models.users import UserResponse
from app.web.deps.database import DatabaseConnection

# Dependency extracts the Bearer token from the Authorization header
access_token_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")  # absence of a token -> 401
optional_access_token_scheme = OAuth2PasswordBearer(tokenUrl="/users/token", auto_error=False)  # absense of a token -> `None`


# dependency
def get_current_user(
    connection: DatabaseConnection,
    token: str = Depends(access_token_scheme),
) -> UserResponse:
    from app.web.users import service

    user = service.get_by_token(connection, token)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    return user


# dependency
def require_anonymous_user(
    connection: DatabaseConnection,
    token: str | None = Depends(optional_access_token_scheme),
) -> None:
    from app.web.users import service

    if token is None:
        return

    user = service.get_by_token(connection, token)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    raise HTTPException(
        status_code=403,
        detail="Authenticated user cannot register another account",
    )


# dependency
def get_current_admin(
    user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )

    return user


CurrentUser = Annotated[
    UserResponse,
    Depends(get_current_user),
]
CurrentAdmin = Annotated[
    UserResponse,
    Depends(get_current_admin),
]
