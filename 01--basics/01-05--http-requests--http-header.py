from fastapi import FastAPI, Header

app = FastAPI()


@app.post("/hi")
def greet(who: str = Header()):
    return f"Hello {who}!"


@app.post("/agent")
def agent(user_agent: str = Header()):
    # Returns the User-Agent from the header
    return user_agent


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01-05--http-requests--http-header:app", reload=True)

# Type in the command line
"""
$ http -v POST localhost:8000/hi who:ax-va
POST /hi HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:8000
User-Agent: HTTPie/3.2.4
who: ax-va



HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Mon, 22 Jun 2026 20:26:35 GMT
server: uvicorn

"Hello ax-va!"


$ http -v POST localhost:8000/agent
POST /agent HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: localhost:8000
User-Agent: HTTPie/3.2.4



HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Mon, 22 Jun 2026 20:25:08 GMT
server: uvicorn

"HTTPie/3.2.4"

"""