from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.models.users import UserToCreate, UserResponse, UserFromDB, UserToDB
from app.repositories.errors import NotFoundError
from app.services import users
from app.services.auth import access_tokens

service = users
router = APIRouter(prefix="/users")

# Dependency extracts the Bearer token from the Authorization header
access_token_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


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


@router.get("")
@router.get("/")
def get_all() -> list[UserResponse]:
    return service.get_all()


@router.get("/me")
@router.get("/me/")
def get_current_user(
    token: str = Depends(access_token_scheme),
) -> UserResponse:
    user = service.get_by_token(token)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.get("/{user_id}")
@router.get("/{user_id}/")
def get_by_id(user_id: int) -> UserResponse:
    user: UserResponse | None = service.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
        )

    return user


@router.get("/{user_id}")
@router.get("/{user_id}/")
def get_by_username(username: str) -> UserResponse:
    user: UserResponse | None = service.get_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with username {username!r} not found",
        )

    return user


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(user: UserToCreate) -> UserResponse:
    return service.create(user)


@router.put("/{user_id}")
@router.put("/{user_id}/")
def replace(user_id: int, user: UserToDB) -> UserResponse:
    try:
        user: UserResponse = service.replace(user_id, user)

    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    return user


@router.patch("/{user_id}")
@router.patch("/{user_id}/")
def modify(explorer_id: int) -> UserResponse:
    raise NotImplementedError()


@router.delete("/{explorer_id}")
@router.delete("/{explorer_id}/")
def delete(explorer_id: int) -> bool:
    deleted = service.delete(explorer_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Explorer with ID {explorer_id} not found",
        )

    return deleted
