from model import Creature
from fastapi import FastAPI

app = FastAPI()


@app.get("/creatures")
def get_all() -> list[Creature]:
    from data import get_creatures
    return get_creatures()


if __name__ == "__main__":

    import uvicorn

    uvicorn.run("web:app", reload=True)


"""
$ http http://localhost:8000/creatures
HTTP/1.1 200 OK
content-length: 211
content-type: application/json
date: Wed, 24 Jun 2026 16:29:43 GMT
server: uvicorn

[
    {
        "aka": "Abominable Snowman",
        "area": "Himalayas",
        "country": "CN",
        "description": "Hirsute Himalayan",
        "name": "yeti"
    },
    {
        "aka": "Bigfoot",
        "area": "*",
        "country": "US",
        "description": "Yeti's Cousin Eddie",
        "name": "sasquatch"
    }
]

"""