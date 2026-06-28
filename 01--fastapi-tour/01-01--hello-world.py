"""
*Path operation functions*
are the functions that are called
when a request is made to a specific path and HTTP method.

aka: endpoint functions, route functions
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")  # path decorator
def greet():  # path operation function
    return "Hello World!"
    # After the path function returns,
    # FastAPI serializes the returned object
    # and wraps it in a `JSONResponse`:
    # 1. Request
    # 2. Path function returns a Python object
    # 3. FastAPI serializes it
    # 4. JSONResponse
    # 5. HTTP response


# 1. Start Uvicorn internally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01-01--hello-world:app", reload=True)


# Or start Uvicorn externally with the command line
"""
$ uvicorn 01-01--hello-world:app --reload
"""
# and CTRL+C to shut down

# Note:
# Using `reload`
# - Development mode
# - Automatically restarts Uvicorn when source files changes
# - Not recommended for production

# 2. Then request with the command line
"""
$ http localhost:8000/hi
HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Sun, 21 Jun 2026 21:15:47 GMT
server: uvicorn

"Hello World!"
"""

# 3. Print only the response body
"""
$ http -b localhost:8000/hi
"Hello World!"
"""
# The same is printed with `--body` or `-p b`.

# 4. Print the whole request header and response header and body
"""
$ http -v localhost:8000/hi
GET /hi HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8000
User-Agent: HTTPie/3.2.4



HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Sun, 21 Jun 2026 21:27:33 GMT
server: uvicorn

"Hello World!"
"""

# 5. Type in the browser
"""
http://localhost:8000/hi
"""

# 6. Type in the Python console
"""
>>> import requests
>>> r = requests.get("http://localhost:8000/hi")
>>> r.json()
'Hello World!'

>>> import httpx
>>> r = httpx.get("http://localhost:8000/hi")
>>> r.json()
'Hello World!'

"""
