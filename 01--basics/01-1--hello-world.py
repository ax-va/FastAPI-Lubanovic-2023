from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")  # path decorator
def greet():  # path function
    return "Hello World!"


# 1. Start Uvicorn internally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01-1--hello-world:app", reload=True)


# Or start Uvicorn externally with the command line
"""
$ uvicorn 01-1--hello-world:app --reload
"""
# and CTRL+C to shut down

"""
Using `reload`
- Development mode
- Automatically restarts Uvicorn when source files changes
- Not recommended for production 
"""

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

# 3. Skip the response headers and print only the body
"""
$ http -b localhost:8000/hi
"Hello World!"
"""

# 4. Get the whole request headers
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
