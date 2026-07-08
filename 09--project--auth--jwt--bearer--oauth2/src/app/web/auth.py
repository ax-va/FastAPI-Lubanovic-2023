from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.models.users import UserResponse

# Dependency extracts the Bearer token from the Authorization header
access_token_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# dependency
def get_current_user(
    token: str = Depends(access_token_scheme),
) -> UserResponse:
    from app.web.users import service

    user = service.get_by_token(token)

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
def get_current_admin(
    user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required",
        )

    return user
