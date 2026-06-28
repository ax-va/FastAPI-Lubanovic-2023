from pydantic import BaseModel


class Explorer(BaseModel):
    id: int
    name: str
    country: str
    description: str
