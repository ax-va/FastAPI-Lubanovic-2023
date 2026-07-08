from fastapi import FastAPI

from app.repositories.sqlite import database as db
from app.services.users import admin_exists, create_admin
from app.web import creatures, explorers, users


db.init()
if not admin_exists():
    print("You must create an admin.")
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_admin(username, password)

app = FastAPI()
app.include_router(creatures.router)
app.include_router(explorers.router)
app.include_router(users.router)


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