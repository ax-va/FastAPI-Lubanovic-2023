from pydantic import BaseModel, Field


# 400
class BadRequestResponse(BaseModel):
    detail: str = Field(
        examples=["Use either `/users/42` or `/users?username=Alice`, but not both"]
    )


# 401
class UnauthorizedResponse(BaseModel):
    detail: str = Field(
        examples=["Incorrect username or password"]
    )


# 404
class NotFoundResponse(BaseModel):
    detail: str = Field(
        examples=[
            "Creature with ID 42 not found",
            "Explorer with ID 42 not found",
            "User with ID 42 not found",
            "User with username 'Alice' not found",
        ]
    )