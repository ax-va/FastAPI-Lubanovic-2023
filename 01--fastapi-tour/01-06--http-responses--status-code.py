from fastapi import FastAPI

app = FastAPI()


@app.get("/happy")
def happy(status_code=200):
    return ":)"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01-06--http-responses--status-code:app", reload=True)


# Type the command line
"""
$ http localhost:8000/happy
HTTP/1.1 200 OK
content-length: 4
content-type: application/json
date: Tue, 23 Jun 2026 11:05:09 GMT
server: uvicorn

":)"

"""