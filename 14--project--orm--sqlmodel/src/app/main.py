from fastapi import FastAPI
from sqlmodel import Session

from app.repositories.sqlalchemy import database as db
from app.services import users as users_service
from app.web import creatures as creatures_web
from app.web import explorers as explorers_web
from app.web import users as users_web

with Session(db.engine) as db_session:
    users_service.ensure_admin_exists(db_session)

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
$ http -b localhost:8000/explorers
[]

$ http -b localhost:8000/explorers name="Ax-Va" country="DE" description="The best German explorer"
{
    "detail": "Not authenticated"
}

$ http -b localhost:8000/users username="ax-va" password="123"
{
    "id": 2,
    "is_active": true,
    "is_admin": false,
    "username": "ax-va"
}

$ http -f localhost:8000/users/token username="ax-va" password="123"
HTTP/1.1 200 OK
content-length: 165
content-type: application/json
date: Fri, 10 Jul 2026 09:52:10 GMT
server: uvicorn

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJheC12YSIsImV4cCI6MTc4MzY3ODAzMH0.PQCGdqJYXLmWTW02liS3blTqSm_iK23C8LpDjxpONpA",
    "token_type": "bearer"
}

$ http -b localhost:8000/explorers \
"Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJheC12YSIsImV4cCI6MTc4MzY3ODAzMH0.PQCGdqJYXLmWTW02liS3blTqSm_iK23C8LpDjxpONpA" \
name="Ax-Va" \
country="DE" \
description="FastAPI explorer"
{
    "country": "DE",
    "description": "FastAPI explorer",
    "id": 1,
    "name": "Ax-Va"
}

$ http -b localhost:8000/users/me "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJheC12YSIsImV4cCI6MTc4MzY3ODAzMH0.PQCGdqJYXLmWTW02liS3blTqSm_iK23C8LpDjxpONpA"
{
    "detail": "Invalid or expired access token"
}

$ http -b localhost:8000/users/2 "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJheC12YSIsImV4cCI6MTc4MzY3OTA1OX0.EPeryjWN5RfcBc3SR9z3tlQ__mtIROVQXfGegSLdeIc"
{
    "detail": "Admin privileges required"
}

$ http -b DELETE localhost:8000/users/me "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJheC12YSIsImV4cCI6MTc4MzY3OTA1OX0.EPeryjWN5RfcBc3SR9z3tlQ__mtIROVQXfGegSLdeIc"
null

$ http -b localhost:8000/explorers
[
    {
        "country": "DE",
        "description": "FastAPI explorer",
        "id": 1,
        "name": "Ax-Va"
    }
]

$ http -f localhost:8000/users/token username="admin" password="admin"
HTTP/1.1 200 OK
content-length: 165
content-type: application/json
date: Fri, 10 Jul 2026 11:48:52 GMT
server: uvicorn

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MzY4NTAzMn0.QVoCxpJpkZ3iYrtswJisIYOvYaWTo9MA_f-Somg06rI",
    "token_type": "bearer"
}

$ http -b localhost:8000/users \
"Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MzY4NTAzMn0.QVoCxpJpkZ3iYrtswJisIYOvYaWTo9MA_f-Somg06rI"
[
    {
        "id": 1,
        "is_active": true,
        "is_admin": true,
        "username": "admin"
    },
    {
        "id": 2,
        "is_active": false,
        "is_admin": false,
        "username": "ax-va"
    }
]

$ http -b PATCH localhost:8000/users/2/grant-admin "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MzY4NTAzMn0.QVoCxpJpkZ3iYrtswJisIYOvYaWTo9MA_f-Somg06rI"
{
    "id": 2,
    "is_active": false,
    "is_admin": true,
    "username": "ax-va"
}

$ http -b localhost:8000/users/2 "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MzY4NTAzMn0.QVoCxpJpkZ3iYrtswJisIYOvYaWTo9MA_f-Somg06rI"
{
    "id": 2,
    "is_active": false,
    "is_admin": true,
    "username": "ax-va"
}

$ http -b PATCH localhost:8000/users/2/revoke-admin "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MzY4NTAzMn0.QVoCxpJpkZ3iYrtswJisIYOvYaWTo9MA_f-Somg06rI"
{
    "id": 2,
    "is_active": false,
    "is_admin": false,
    "username": "ax-va"
}

$ http -b localhost:8000/creatures \
"Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MzY4NTAzMn0.QVoCxpJpkZ3iYrtswJisIYOvYaWTo9MA_f-Somg06rI" \
name="Lubanovic" \
country="US" \
area="North America" \
description="Python creature" aka="Author"
{
    "aka": "Author",
    "area": "North America",
    "country": "US",
    "description": "Python creature",
    "id": 1,
    "name": "Lubanovic"
}

$ http -b POST localhost:8000/explorers/1/creatures/1 \
"Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MzY4NTAzMn0.QVoCxpJpkZ3iYrtswJisIYOvYaWTo9MA_f-Somg06rI"
[
    {
        "aka": "Author",
        "area": "North America",
        "country": "US",
        "description": "Python creature",
        "id": 1,
        "name": "Lubanovic"
    }
]

$ http -b localhost:8000/explorers/1/creatures
[
    {
        "aka": "Author",
        "area": "North America",
        "country": "US",
        "description": "Python creature",
        "id": 1,
        "name": "Lubanovic"
    }
]

$ http -b localhost:8000/creatures/1/explorers
[
    {
        "country": "DE",
        "description": "FastAPI explorer",
        "id": 1,
        "name": "Ax-Va"
    }
]

$ http -b POST localhost:8000/explorers/1/creatures/1 \
"Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4MzY4NTAzMn0.QVoCxpJpkZ3iYrtswJisIYOvYaWTo9MA_f-Somg06rI"
{
    "detail": "Explorer with ID 1 is already bound to creature with ID 1"
}

"""