from pydantic import BaseModel


class UserToCreateRequest(BaseModel):
    username: str
    password: str


class UserToReplaceRequest(BaseModel):
    username: str
    password: str
    is_active: bool


class UserToDB(BaseModel):
    username: str
    password_hash: str
    is_active: bool
    is_admin: bool


class UserFromDB(BaseModel):
    id: int
    username: str
    password_hash: str
    is_active: bool
    is_admin: bool


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
    is_admin: bool
