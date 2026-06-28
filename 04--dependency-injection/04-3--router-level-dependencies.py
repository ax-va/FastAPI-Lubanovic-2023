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
from fastapi import FastAPI, Depends, Query, HTTPException, APIRouter

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

user_router = APIRouter(
    prefix="/users",
    dependencies=[Depends(check_dep)],
)


@user_router.get("/profile")
def get_profile() -> dict:
    return {"page": "profile"}


@user_router.get("/settings")
def get_profile() -> dict:
    return {"page": "settings"}


app.include_router(user_router)


if __name__ == "__main__":

    import uvicorn

    uvicorn.run("04-3--router-level-dependencies:app", reload=True)


"""
$ http http://localhost:8000/users/profile name==AxVa
HTTP/1.1 200 OK
content-length: 18
content-type: application/json
date: Thu, 25 Jun 2026 21:43:45 GMT
server: uvicorn

{
    "page": "profile"
}

$ http http://localhost:8000/users/settings name==AxVa
HTTP/1.1 200 OK
content-length: 19
content-type: application/json
date: Thu, 25 Jun 2026 21:44:10 GMT
server: uvicorn

{
    "page": "settings"
}

$ http http://localhost:8000/users/profile name==ax-va
HTTP/1.1 404 Not Found
content-length: 27
content-type: application/json
date: Thu, 25 Jun 2026 21:44:32 GMT
server: uvicorn

{
    "detail": "User not found"
}

"""