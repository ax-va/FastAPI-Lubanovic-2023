from fastapi import FastAPI

from app.repositories.sqlite import database as db
from app.services import users as users_service
from app.web import creatures as creatures_web
from app.web import explorers as explorers_web
from app.web import users as users_web


db.init()
users_service.ensure_admin_exists()

app = FastAPI()
app.include_router(creatures_web.router)
app.include_router(explorers_web.router)
app.include_router(users_web.router)


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

"""