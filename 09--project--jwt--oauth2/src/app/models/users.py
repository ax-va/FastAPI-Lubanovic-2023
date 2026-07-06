from pydantic import BaseModel


class UserToCreate(BaseModel):
    username: str
    password: str


class UserToDB(BaseModel):
    id: int
    username: str
    password_hash: str
    is_active: bool


class UserFromDB(BaseModel):
    id: int
    username: str
    password_hash: str
    is_active: bool


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
