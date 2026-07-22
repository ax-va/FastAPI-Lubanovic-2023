from fastapi import FastAPI

from app.repositories.sqlite import database as db
from app.repositories.sqlite.database import connection_manager
from app.web import creatures as creatures_web
from app.web import explorers as explorers_web

with connection_manager() as connection:
    db.init(connection)

app = FastAPI()
app.include_router(creatures_web.router)
app.include_router(explorers_web.router)


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
$ http -b localhost:8000/explorers
[]

$ http -b localhost:8000/explorers name="Ax-Va" country="DE" description="The best German explorer"
{
    "country": "DE",
    "description": "The best German explorer",
    "id": 1,
    "name": "Ax-Va"
}

"""