from datetime import datetime, UTC

from fastapi import FastAPI, HTTPException

from model.tag import TagIn, Tag, TagOut
from service.tag import create_tag, get_tag

app = FastAPI()


@app.post('/', response_model=TagOut)
def create_one(tag_in: TagIn) -> TagOut:
    tag_obj: Tag = Tag(tag=tag_in.tag, created=datetime.now(UTC), secret="123")
    create_tag(tag_obj)
    return tag_obj


@app.get('/{tag_str}', response_model=TagOut)
def get_one(tag_str: str) -> TagOut:
    tag_obj: Tag = get_tag(tag_str)

    if tag_obj is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag_obj
