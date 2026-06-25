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
    prefix="/user",
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

    uvicorn.run("04-3--multiple-paths--router:app", reload=True)


"""
$ http http://localhost:8000/user/profile name==AxVa
HTTP/1.1 200 OK
content-length: 18
content-type: application/json
date: Thu, 25 Jun 2026 21:43:45 GMT
server: uvicorn

{
    "page": "profile"
}

$ http http://localhost:8000/user/settings name==AxVa
HTTP/1.1 200 OK
content-length: 19
content-type: application/json
date: Thu, 25 Jun 2026 21:44:10 GMT
server: uvicorn

{
    "page": "settings"
}

$ http http://localhost:8000/user/profile name==ax-va
HTTP/1.1 404 Not Found
content-length: 27
content-type: application/json
date: Thu, 25 Jun 2026 21:44:32 GMT
server: uvicorn

{
    "detail": "User not found"
}

"""