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
from fastapi import FastAPI, Depends

def dep1():
    print("Dependency 1")

def dep2():
    print("Dependency 2")


app = FastAPI(
    dependencies=[
        Depends(dep1),
        Depends(dep2),
    ]
)


@app.get("/users")
def get_users():
    return ["Alice", "Bob", "Carol"]


@app.get("/books")
def get_books():
    return ["Book 1", "Book 2", "Book 3"]


if __name__ == "__main__":

    import uvicorn

    uvicorn.run("04-4--app-level-dependencies:app", reload=True)


"""
$ http http://localhost:8000/users
HTTP/1.1 200 OK
content-length: 23
content-type: application/json
date: Thu, 25 Jun 2026 21:53:13 GMT
server: uvicorn

[
    "Alice",
    "Bob",
    "Carol"
]

$ http http://localhost:8000/books
HTTP/1.1 200 OK
content-length: 28
content-type: application/json
date: Thu, 25 Jun 2026 21:53:37 GMT
server: uvicorn

[
    "Book 1",
    "Book 2",
    "Book 3"
]

"""
