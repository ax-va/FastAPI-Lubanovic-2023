"""
HTTP Basic Authentication is insecure over HTTP
because usernames and passwords are only Base64-encoded, not encrypted.
It should always be used together with HTTPS to protect credentials from interception.
"""
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

username: str = "ax-va"
password: str = "123"

# The instance has the `__call__` method
http_basic = HTTPBasic()  


@app.get("/who")
def get_user(creds: HTTPBasicCredentials = Depends(http_basic)) -> dict:
    if (
        creds.username == username
        and creds.password == password
    ):
        return {
            "username": creds.username,
            "password": creds.password,
        }
    raise HTTPException(status_code=401, detail="Unauthorized")  # meaning unauthenticated


if __name__ == "__main__":
    uvicorn.run("08-1--http-basic-auth:app", reload=True)


"""
$ http -a ax-va:123 localhost:8000/who
HTTP/1.1 200 OK
content-length: 37
content-type: application/json
date: Sun, 05 Jul 2026 15:14:36 GMT
server: uvicorn

{
    "password": "123",
    "username": "ax-va"
}

$ http -a ax-va:abc localhost:8000/who
HTTP/1.1 401 Unauthorized
content-length: 25
content-type: application/json
date: Sun, 05 Jul 2026 15:16:28 GMT
server: uvicorn

{
    "detail": "Unauthorized"
}

"""

"""
>>> import requests
>>> r = requests.get("http://localhost:8000/who", auth=("ax-va", "123"))
>>> r.json()
{'username': 'ax-va', 'password': '123'}

"""