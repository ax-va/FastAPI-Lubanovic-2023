from datetime import datetime
from pydantic import BaseModel


# input data
class TagIn(BaseModel):
    tag: str


# inner data
class Tag(BaseModel):
    tag: str
    created: datetime
    secret: str


# public date
class TagOut(BaseModel):
    tag: str
    created: datetime
