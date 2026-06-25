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
"""
from fastapi import FastAPI, Depends, Query, HTTPException

db = {
    "AxVa": {"valid": True},
}

app = FastAPI()


# dependency function (guard)
def check_dep(name: str = Query(...)) -> None:
    if name not in db:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

# Note:
# `...` (ellipsis) is used by FastAPI and Pydantic to indicate
# that a parameter or field is required and has no default value.


# path operation function
@app.get("/check_user", dependencies=[Depends(check_dep)])
def check_user() -> bool:
    return True


if __name__ == "__main__":

    import uvicorn

    uvicorn.run("04-2--dependency-as-guard:app", reload=True)


"""
$ http http://localhost:8000/check_user name==AxVa
HTTP/1.1 200 OK
content-length: 4
content-type: application/json
date: Thu, 25 Jun 2026 21:32:20 GMT
server: uvicorn

true

$ http http://localhost:8000/check_user name==ax-va
HTTP/1.1 404 Not Found
content-length: 27
content-type: application/json
date: Thu, 25 Jun 2026 21:32:37 GMT
server: uvicorn

{
    "detail": "User not found"
}

"""
