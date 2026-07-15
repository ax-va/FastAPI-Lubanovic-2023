from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import access_tokens
from app.models.users import UserToCreate, UserResponse, UserFromDB, UserToReplace
from app.repositories.errors import NotFoundError
from app.services import users as users_service
from app.web.deps.auth import get_current_user, get_current_admin, reject_authenticated_user
from app.web.errors import resource_with_id_not_found
from app.web.metadata import UNAUTHORIZED, NOT_FOUND, BAD_REQUEST

service = users_service
router = APIRouter(prefix="/users", tags=["Users"])

# OAuth2 token endpoint.
# Clients send username and password here to obtain an access token.
@router.post(
    "/token",
    responses=UNAUTHORIZED,
)
def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """Authenticates a user and returns a JWT access token."""

    user: UserFromDB | None = service.authenticate_user(form_data.username, form_data.password)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {"sub": user.username}
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
    user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    return user


# API only for authenticated admins
@router.patch(
    "/{user_id}/grant-admin",
    responses=NOT_FOUND,
)
def grant_admin(
    user_id: int,
    _: UserResponse = Depends(get_current_admin),
) -> UserResponse:
    try:
        user: UserResponse = service.set_admin(user_id, True)

    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return user


# API only for authenticated admins
@router.patch(
    "/{user_id}/revoke-admin",
    responses=NOT_FOUND,
)
def revoke_admin(
    user_id: int,
    _: UserResponse = Depends(get_current_admin),
) -> UserResponse:
    try:
        user: UserResponse = service.set_admin(user_id, False)

    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return user


# API only for authenticated admins
@router.get("")
@router.get(
    "/{user_id}",
    responses=BAD_REQUEST | NOT_FOUND,
)
def get(
    user_id: int | None = None,  # example: `GET /users/1`
    username: str | None = Query(default=None, min_length=1),  # example: `GET /users?useranme=Alice`
    _: UserResponse = Depends(get_current_admin),
) -> UserResponse | list[UserResponse]:

    if user_id is not None and username is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Use either `/users/{user_id}` or `/users?username={username}`, but not both",
        )

    if user_id is not None:
        user: UserResponse | None = service.get_by_id(user_id)

        if user is None:
            raise resource_with_id_not_found("User", user_id)

        return user

    elif username is not None:
        user: UserResponse | None = service.get_by_username(username)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"User with username {username!r} not found",
            )

        return user

    else:
        users: list[UserResponse] = service.get_all()
        return users


# public API
@router.post("", status_code=201)  # 201 Created
def create(
    user: UserToCreate,
    _: None = Depends(reject_authenticated_user)
) -> UserResponse:
    return service.create(user)


# API only for authenticated admins
@router.put(
    "/{user_id}",
    responses=NOT_FOUND,
)
def replace(
    user_id: int,
    user: UserToReplace,
    _: UserResponse = Depends(get_current_admin),
) -> UserResponse:
    try:
        user: UserResponse = service.replace(user_id, user)

    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return user


# NOTE:
# Keep "/users/me" above "/users/{user_id}".
# FastAPI matches routes in declaration order.
# Otherwise, "/users/me" will be matched by the dynamic route first.

# API for only authenticated users
@router.delete("/me")
def delete_me(
    user: UserResponse = Depends(get_current_user)
) -> bool:
    return service.delete(user.id)


# API only for authenticated admins
@router.delete(
    "/{user_id}",
    responses=NOT_FOUND,
)
def delete(
    user_id: int,
    _: UserResponse = Depends(get_current_admin),
) -> bool:
    deleted = service.delete(user_id)
    if not deleted:
        raise resource_with_id_not_found("User", user_id)

    return deleted
