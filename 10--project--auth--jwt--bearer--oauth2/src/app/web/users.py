from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import access_tokens
from app.models.schemas.users import UserToCreateRequest, UserResponse, UserToReplaceRequest
from app.services import users as users_service
from app.services.errors import LastAdminError, NotFoundError, DuplicateError
from app.web.deps.auth import require_anonymous_user, CurrentUser, CurrentAdmin
from app.web.deps.database import DatabaseConnection
from app.web.errors import resource_with_id_not_found

service = users_service
router = APIRouter(prefix="/users", tags=["Users"])


# OAuth2 token endpoint.
# Clients send username and password here to obtain an access token.
@router.post("/token")
def create_access_token(
    db_connection: DatabaseConnection,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """Authenticates a user and returns a JWT access token."""

    is_verified: bool = service.verify_credentials(
        db_connection,
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
@router.get("/me")
def get_me(
    user_response: CurrentUser
) -> UserResponse:
    return user_response


# API only for authenticated admins
@router.patch("/{user_id}/grant-admin")
def grant_admin(
    db_connection: DatabaseConnection,
    user_id: int,
    _: CurrentAdmin,
) -> UserResponse:
    try:
        user_response: UserResponse = service.set_admin(db_connection, user_id, True)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    return user_response


# API only for authenticated admins
@router.patch("/{user_id}/revoke-admin")
def revoke_admin(
    db_connection: DatabaseConnection,
    user_id: int,
    _: CurrentAdmin,
) -> UserResponse:
    try:
        user_response: UserResponse = service.set_admin(db_connection, user_id, False)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    except LastAdminError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e

    return user_response


# API only for authenticated admins
@router.get("")
@router.get("/{user_id}")
def get(
    db_connection: DatabaseConnection,
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
        user_response: UserResponse | None = service.get_by_id(db_connection, user_id)

        if user_response is None:
            raise resource_with_id_not_found(f"User with ID {user_id} not found")

        return user_response

    elif username is not None:
        user_response: UserResponse | None = service.get_by_username(db_connection, username)

        if user_response is None:
            raise resource_with_id_not_found(f"User with username {username!r} not found")

        return user_response

    else:
        user_responses: list[UserResponse] = service.get_all(db_connection)
        return user_responses


# public API
@router.post(
    "",
    status_code=201,  # 201 Created
)
def create(
    db_connection: DatabaseConnection,
    user_request: UserToCreateRequest,
    _: None = Depends(require_anonymous_user)
) -> UserResponse:
    try:
        created: UserResponse = service.create(db_connection, user_request)

    except DuplicateError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e

    return created


# API only for authenticated admins
@router.put("/{user_id}")
def replace(
    db_connection: DatabaseConnection,
    user_id: int,
    user_request: UserToReplaceRequest,
    _: CurrentAdmin,
) -> UserResponse:
    try:
        updated: UserResponse = service.replace(db_connection, user_id, user_request)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    except DuplicateError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e

    return updated


# NOTE:
# Keep "/users/me" above "/users/{user_id}".
# FastAPI matches routes in declaration order.
# Otherwise, "/users/me" will be matched by the dynamic route first.

# API for only authenticated users
@router.delete("/me")
def soft_delete_me(
    db_connection: DatabaseConnection,
    user_response: CurrentUser,
) -> UserResponse:
    try:
        soft_deleted: UserResponse = service.soft_delete(db_connection, user_response.id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    except LastAdminError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e

    return soft_deleted


# API only for authenticated admins
@router.delete("/{user_id}")
def soft_delete(
    db_connection: DatabaseConnection,
    user_id: int,
    _: CurrentAdmin,
) -> UserResponse:
    try:
        soft_deleted: UserResponse = service.soft_delete(db_connection, user_id)

    except NotFoundError as e:
        raise resource_with_id_not_found(str(e)) from e

    except LastAdminError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from e

    return soft_deleted
