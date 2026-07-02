from fastapi import FastAPI

from app.web import creatures
from app.web import explorers

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
