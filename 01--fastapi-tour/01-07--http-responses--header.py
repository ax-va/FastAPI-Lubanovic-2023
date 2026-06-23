from fastapi import FastAPI, Response

app = FastAPI()


# Inject to the HTTP response headers
@app.get("/header/{name}/{value}")
def header(name: str, value: str, response: Response):
    response.headers[name] = value
    return "normal body"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01-07--http-responses--header:app", reload=True)


# Type the command line
"""
$ http localhost:8000/header/marco/polo
HTTP/1.1 200 OK
content-length: 13
content-type: application/json
date: Tue, 23 Jun 2026 11:14:08 GMT
marco: polo
server: uvicorn

"normal body"

"""