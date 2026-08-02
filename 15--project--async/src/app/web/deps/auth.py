from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.models.schemas.users import UserResponse
from app.web.deps.database import DatabaseSession

# Dependency extracts the Bearer token from the Authorization header
access_token_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")  # absence of a token -> 401
optional_access_token_scheme = OAuth2PasswordBearer(tokenUrl="/users/token", auto_error=False)  # absense of a token -> `None`


# dependency
def get_current_user(
    db_session: DatabaseSession,
    token: str = Depends(access_token_scheme),
) -> UserResponse:
    from app.web.users import service

    user_response = service.get_by_token(db_session, token)

    if user_response is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_response.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    return user_response


# dependency
def require_anonymous_user(
    db_session: DatabaseSession,
    token: str | None = Depends(optional_access_token_scheme),
) -> None:
    from app.web.users import service

    if token is None:
        return

    user_response = service.get_by_token(db_session, token)

    if user_response is None:
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
    user_response: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if not user_response.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )

    return user_response


CurrentUser = Annotated[
    UserResponse,
    Depends(get_current_user),
]
CurrentAdmin = Annotated[
    UserResponse,
    Depends(get_current_admin),
]
