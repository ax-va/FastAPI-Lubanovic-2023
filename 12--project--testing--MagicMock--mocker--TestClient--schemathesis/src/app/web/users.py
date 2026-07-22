from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import access_tokens
from app.models.users import UserToCreateRequest, UserResponse, UserToReplaceRequest
from app.services import users as users_service
from app.services.errors import LastAdminError, NotFoundError, DuplicateError
from app.web.deps.auth import CurrentUser, CurrentAdmin, require_anonymous_user
from app.web.deps.database import DatabaseConnection
from app.web.errors import resource_with_id_not_found
from app.web.metadata import UNAUTHORIZED, NOT_FOUND, BAD_REQUEST, CONFLICT

service = users_service
router = APIRouter(prefix="/users", tags=["Users"])

# OAuth2 token endpoint.
# Clients send username and password here to obtain an access token.
@router.post(
    "/token",
    responses=UNAUTHORIZED,
)
def create_access_token(
    connection: DatabaseConnection,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """Authenticates a user and returns a JWT access token."""

    is_verified: bool = service.verify_credentials(
        connection,
        form_data.username,
        form_data.password
    )

    if not is_verified:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {"sub": form_data.username}
    access_token = access_tokens.create_access_token(data=data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# NOTE:
# Keep "/users/me" above "/users/{user_id}".
# FastAPI matches routes in declaration order.
# Otherwise, "/users/me" will be matched by the dynamic route first.

# API for only authenticated users
@router.get(
    "/me",
    responses=UNAUTHORIZED,
)
def get_me(
    user: CurrentUser
) -> UserResponse:
    return user


# API only for authenticated admins
@router.patch(
    "/{user_id}/grant-admin",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def grant_admin(
    connection: DatabaseConnection,
    user_id: int,
    _: CurrentAdmin,
) -> UserResponse:
    try:
        user: UserResponse = service.set_admin(connection, user_id, True)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    return user


# API only for authenticated admins
@router.patch(
    "/{user_id}/revoke-admin",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def revoke_admin(
    connection: DatabaseConnection,
    user_id: int,
    _: CurrentAdmin,
) -> UserResponse:
    try:
        user: UserResponse = service.set_admin(connection, user_id, False)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    except LastAdminError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e

    return user


# API only for authenticated admins
@router.get(
    "",
    responses=UNAUTHORIZED | BAD_REQUEST | NOT_FOUND,
)
@router.get(
    "/{user_id}",
    responses=UNAUTHORIZED | BAD_REQUEST | NOT_FOUND,
)
def get(
    connection: DatabaseConnection,
    _: CurrentAdmin,
    user_id: int | None = None,  # example: `GET /users/1`
    username: str | None = Query(default=None, min_length=1),  # example: `GET /users?useranme=Alice`
) -> UserResponse | list[UserResponse]:
    if user_id is not None and username is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Use either `/users/{user_id}` or `/users?username={username}`, but not both",
        )

    if user_id is not None:
        user: UserResponse | None = service.get_by_id(connection, user_id)

        if user is None:
            raise resource_with_id_not_found(f"User with ID {user_id} not found")

        return user

    elif username is not None:
        user: UserResponse | None = service.get_by_username(connection, username)

        if user is None:
            raise resource_with_id_not_found(f"User with username {username!r} not found")

        return user

    else:
        users: list[UserResponse] = service.get_all(connection)
        return users


# public API
@router.post(
    "",
    status_code=201,  # 201 Created
    responses=UNAUTHORIZED | CONFLICT,
)
def create(
    connection: DatabaseConnection,
    user: UserToCreateRequest,
    _: None = Depends(require_anonymous_user)
) -> UserResponse:
    try:
        user: UserResponse = service.create(connection, user)

    except DuplicateError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e

    return user


# API only for authenticated admins
@router.put(
    "/{user_id}",
    responses=UNAUTHORIZED | NOT_FOUND,
)
def replace(
    connection: DatabaseConnection,
    user_id: int,
    user: UserToReplaceRequest,
    _: CurrentAdmin,
) -> UserResponse:
    try:
        user: UserResponse = service.replace(connection, user_id, user)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    except DuplicateError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e

    return user


# NOTE:
# Keep "/users/me" above "/users/{user_id}".
# FastAPI matches routes in declaration order.
# Otherwise, "/users/me" will be matched by the dynamic route first.

# API for only authenticated users
@router.delete(
    "/me",
    responses=UNAUTHORIZED | CONFLICT,
)
def delete_me(
    connection: DatabaseConnection,
    user: CurrentUser,
) -> None:
    try:
        service.delete(connection, user.id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    except LastAdminError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e


# API only for authenticated admins
@router.delete(
    "/{user_id}",
    responses=UNAUTHORIZED | NOT_FOUND | CONFLICT,
)
def delete_me(
    connection: DatabaseConnection,
    user: CurrentUser,
) -> None:
    try:
        service.delete(connection, user.id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    except LastAdminError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e
