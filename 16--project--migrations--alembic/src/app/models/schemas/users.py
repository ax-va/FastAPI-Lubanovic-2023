from pydantic import BaseModel


class UserToCreateRequest(BaseModel):
    username: str
    password: str


class UserToReplaceRequest(BaseModel):
    username: str
    password: str
    is_active: bool


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    is_admin: bool
