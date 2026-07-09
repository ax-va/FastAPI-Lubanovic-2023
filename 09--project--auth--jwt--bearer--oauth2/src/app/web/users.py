from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import access_tokens
from app.models.users import UserToCreate, UserResponse, UserFromDB, UserToDB
from app.repositories.errors import NotFoundError
from app.services import users
from app.web.deps.auth import get_current_user, get_current_admin

service = users
router = APIRouter(prefix="/users")

# OAuth2 token endpoint.
# Clients send username and password here to obtain an access token.
@router.post("/token")
@router.post("/token/")
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


# API only for authenticated admins
@router.get("")
@router.get("/")
def get_all(
    admin: UserResponse = Depends(get_current_admin),
) -> list[UserResponse]:
    return service.get_all()


# API for only authenticated users
@router.get("/me")
@router.get("/me/")
def get_me(
    user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    return user


# API only for authenticated admins
@router.get("/{user_id}")
@router.get("/{user_id}/")
def get_by_id(
    user_id: int,
    admin: UserResponse = Depends(get_current_admin),
) -> UserResponse:
    user: UserResponse | None = service.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )

    return user


# API only for authenticated admins
@router.get("/{username}")
@router.get("/{username}/")
def get_by_username(
    username: str,
    admin: UserResponse = Depends(get_current_admin),
) -> UserResponse:
    user: UserResponse | None = service.get_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with username {username!r} not found",
        )

    return user


# public API
@router.post("", status_code=201)  # 201 Created
@router.post("/", status_code=201)
def create(
    user: UserToCreate,
) -> UserResponse:
    return service.create(user)


# API only for authenticated admins
@router.put("/{user_id}")
@router.put("/{user_id}/")
def replace(
    user_id: int,
    user: UserToDB,
    admin: UserResponse = Depends(get_current_admin),
) -> UserResponse:
    try:
        user: UserResponse = service.replace(user_id, user)

    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return user


# API only for authenticated admins
@router.patch("/{user_id}/grand-admin")
@router.patch("/{user_id}/grand-admin/")
def grand_admin(
    user_id: int,
    admin: UserResponse = Depends(get_current_admin),
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
@router.patch("/{user_id}/revoke-admin")
@router.patch("/{user_id}/revoke-admin/")
def revoke_admin(
    user_id: int,
    admin: UserResponse = Depends(get_current_admin),
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
@router.delete("/{user_id}")
@router.delete("/{user_id}/")
def delete(
    user_id: int,
    admin: UserResponse = Depends(get_current_admin),
) -> bool:
    deleted = service.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )

    return deleted
