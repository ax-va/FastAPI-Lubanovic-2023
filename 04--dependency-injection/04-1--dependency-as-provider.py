"""
- *Dependency Injection* is a design pattern in which an object or function receives its dependencies from the outside
instead of creating them itself.

- Dependencies are injected, not instantiated.

- FastAPI implements DI with `Depends()`:
dependency functions are called automatically when your path operation function is called,
and they (dependency functions) return values are injected into your path operation function.
`Depends()` only tells FastAPI where that value comes from.

- FastAPI's dependency injection is more than just passing objects.
Dependency functions benefit from the same automatic validation, type conversion,
and documentation generation as path operation functions.

- In FastAPI, there are dependencies on three levels: endpoint, router, and application.
"""

from fastapi import FastAPI, Depends, Query

app = FastAPI()


# dependency function (provider)
def user_dep(name: str = Query(...), password: str = Query(...)) -> dict:
    return {"name": name, "valid": True}

# Note:
# `...` (ellipsis) is used by FastAPI and Pydantic to indicate
# that a parameter or field is required and has no default value.


# path operation function
@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    return user


if __name__ == "__main__":

    import uvicorn

    uvicorn.run("04-1--dependency-as-provider:app", reload=True)


# HTTPie uses whitespaces and `==` for query parameters
# meaning `/user?name=AxVa&password=12345`.
"""
$ http http://localhost:8000/user name==AxVa password==12345
HTTP/1.1 200 OK
content-length: 28
content-type: application/json
date: Thu, 25 Jun 2026 20:56:07 GMT
server: uvicorn

{
    "name": "AxVa",
    "valid": true
}

"""
