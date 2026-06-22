from fastapi import FastAPI

app = FastAPI()


@app.get("/hi/{who}")
def greet(who):
    return f"Hello {who}!"


# 1. Start Uvicorn internally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01-02--http-requests--url-path:app", reload=True)


# Or start Uvicorn externally with the command line
"""
$ uvicorn 01-02--http-requests--url-path:app --reload
"""
# and CTRL+C to shut down

# 2. Type in the browser
"""
http://localhost:8000/hi/AxVa
"""

# 3. Type in the command line
"""
$ http localhost:8000/hi/ax-va
HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Mon, 22 Jun 2026 17:12:13 GMT
server: uvicorn

"Hello ax-va!"

"""

# 4. Type in the Python console
"""
>>> import requests
>>> r = requests.get("http://localhost:8000/hi/Mom")
>>> r.json()
Hello Mom!'

"""
