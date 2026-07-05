from fastapi import FastAPI

from app.repositories.sqlite import database as db
from app.web import creatures
from app.web import explorers

db.init()

app = FastAPI()
app.include_router(creatures.router)
app.include_router(explorers.router)


@app.get("/")
def top():
    return "top here"


@app.get("/echo/{thing}")
def echo(thing):
    return f"echoing {thing}"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", reload=True)


"""
$ http localhost:8000
HTTP/1.1 200 OK
content-length: 10
content-type: application/json
date: Fri, 03 Jul 2026 16:17:43 GMT
server: uvicorn

"top here"


$ http -b localhost:8000/explorers
[]

$ http -b localhost:8000/explorers name="Ax-Va" country="DE" description="The best German explorer"
{
    "country": "DE",
    "description": "The best German explorer",
    "id": 1,
    "name": "Ax-Va"
}

$ http -b localhost:8000/explorers
[
    {
        "country": "DE",
        "description": "The best German explorer",
        "id": 1,
        "name": "Ax-Va"
    }
]

$ http -b localhost:8000/explorers/1
{
    "country": "DE",
    "description": "The best German explorer",
    "id": 1,
    "name": "Ax-Va"
}

$ http -b PUT localhost:8000/explorers/1 name="AxVa" country="DE" description="*"
{
    "country": "DE",
    "description": "*",
    "id": 1,
    "name": "AxVa"
}

$ http -b DELETE localhost:8000/explorers/1
true

$ http -b localhost:8000/explorers/1
{
    "detail": "Explorer with ID 1 not found"
}

$ http -b localhost:8000/explorers
[]

"""