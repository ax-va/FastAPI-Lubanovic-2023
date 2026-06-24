from datetime import datetime, UTC

from fastapi import FastAPI, HTTPException

from model import TagIn, Tag, TagOut
from service import create_tag, get_tag

app = FastAPI()


# Even though the path functions return `Tag`,
# `response_model` will convert it to a `TagOut`.

@app.post('/', response_model=TagOut)
def create_one(tag_in: TagIn) -> Tag:
    tag_obj: Tag = Tag(tag=tag_in.tag, created=datetime.now(UTC), secret="123")
    create_tag(tag_obj)
    return tag_obj


@app.get('/{tag_str}', response_model=TagOut)
def get_one(tag_str: str) -> Tag:
    tag_obj: Tag = get_tag(tag_str)

    if tag_obj is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag_obj


if __name__ == "__main__":

    import uvicorn

    uvicorn.run("web:app", reload=True)


# Type the command line
"""
$ http localhost:8000/ tag=ax-va
HTTP/1.1 200 OK
content-length: 55
content-type: application/json
date: Wed, 24 Jun 2026 08:56:26 GMT
server: uvicorn

{
    "created": "2026-06-24T08:56:26.862715Z",
    "tag": "ax-va"
}

$ http localhost:8000/ax-va
HTTP/1.1 200 OK
content-length: 55
content-type: application/json
date: Wed, 24 Jun 2026 09:05:19 GMT
server: uvicorn

{
    "created": "2026-06-24T09:05:16.978603Z",
    "tag": "ax-va"
}

$ http localhost:8000/AxVa
HTTP/1.1 404 Not Found
content-length: 26
content-type: application/json
date: Wed, 24 Jun 2026 09:05:53 GMT
server: uvicorn

{
    "detail": "Tag not found"
}

"""
