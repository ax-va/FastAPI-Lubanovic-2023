from fastapi import FastAPI, Body

app = FastAPI()


@app.post("/hi")
def greet(who: str = Body(embed=True)):
    # Get the value of `who` from the JSON-formatted request body
    return f"Hello {who}!"



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01-04--http-requests--body:app", reload=True)

# 1. Type the command line and use the single equal sign `=` to send JSON data.
# So HTTPie automatically recognize as the POST request.
"""
$ http -v localhost:8000/hi who=AxVa
POST /hi HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 15
Content-Type: application/json
Host: localhost:8000
User-Agent: HTTPie/3.2.4

{
    "who": "AxVa"
}


HTTP/1.1 200 OK
content-length: 13
content-type: application/json
date: Mon, 22 Jun 2026 17:43:30 GMT
server: uvicorn

"Hello AxVa!"

"""

# 2. Type in the Python console
"""
>>> import requests
>>> r = requests.post("http://localhost:8000/hi", json={"who": "Mom"})
>>> r.json()
'Hello Mom!'

"""


