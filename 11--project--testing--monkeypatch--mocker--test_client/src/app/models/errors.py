from pydantic import BaseModel, Field


# 400
class BadRequestResponse(BaseModel):
    detail: str = Field(
        examples=[
            "Use either `/users/1` or `/users?username=admin`, but not both",
        ]
    )


# 401
class UnauthorizedResponse(BaseModel):
    detail: str = Field(
        examples=[
            "Incorrect username or password",
            "Invalid or expired access token",
        ]
    )


# 404
class NotFoundResponse(BaseModel):
    detail: str = Field(
        examples=[
            "Creature with ID 1 not found",
            "Explorer with ID 1 not found",
            "User with ID 1 not found",
            "User with username 'admin' not found",
        ]
    )


# 409
class ConflictResponse(BaseModel):
    detail: str = Field(
        examples=[
            "Username 'admin' already exists",
            "Revoking the last admin is not allowed",
            "Deleting the last admin is not allowed",
        ]
    )