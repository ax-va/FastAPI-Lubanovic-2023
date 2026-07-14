from pydantic import BaseModel, Field


class NotFoundResponse(BaseModel):
    detail: str = Field(
        examples=["Resource with ID 42 not found"]
    )