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

# `The ampersand `&` at the end puts the program into the background,
# and you can run other programs in the same terminal window:
"""
$ python -m app.main &
INFO:     Will watch for changes in these directories: ['.../FastAPI-Lubanovic-2023/05--web-layer/src/app']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [389026] using StatReload
INFO:     Started server process [389038]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

"""
# Shut down the server
"""
$ lsof -i :8000
$ kill <pid>
"""

# Open docs in the browser
"""
localhost:8000/docs
"""

# Access the site in the same terminal
"""
$ http localhost:8000
INFO:     127.0.0.1:35700 - "GET / HTTP/1.1" 200 OK
HTTP/1.1 200 OK
content-length: 10
content-type: application/json
date: Sun, 28 Jun 2026 11:16:14 GMT
server: uvicorn

"top here"

$ http -b localhost:8000/echo/ax-va
INFO:     127.0.0.1:52468 - "GET /echo/ax-va HTTP/1.1" 200 OK
"echoing ax-va"

$ http -b localhost:8000/explorers
[
    {
        "country": "FR",
        "description": "Scarce during full moons",
        "id": 1,
        "name": "Claude Hande"
    },
    {
        "country": "DE",
        "description": "Myopic machete man",
        "id": 2,
        "name": "Noah Weiser"
    }
]

$ http -b localhost:8000/explorers/1
{
    "country": "FR",
    "description": "Scarce during full moons",
    "id": 1,
    "name": "Claude Hande"
}

"""