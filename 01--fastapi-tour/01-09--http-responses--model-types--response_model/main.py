if __name__ == "__main__":

    import uvicorn

    uvicorn.run("web.tag:app", reload=True)


# Type the command line
"""
$ http localhost:8000/ tag=ax-va
HTTP/1.1 200 OK
content-length: 55
content-type: application/json
date: Wed, 24 Jun 2026 08:56:26 GMT
server: uvicorn

{
    "created": "2026-06-24T08:56:26.862715Z",
    "tag": "ax-va"
}

$ http localhost:8000/ax-va
HTTP/1.1 200 OK
content-length: 55
content-type: application/json
date: Wed, 24 Jun 2026 09:05:19 GMT
server: uvicorn

{
    "created": "2026-06-24T09:05:16.978603Z",
    "tag": "ax-va"
}

$ http localhost:8000/AxVa
HTTP/1.1 404 Not Found
content-length: 26
content-type: application/json
date: Wed, 24 Jun 2026 09:05:53 GMT
server: uvicorn

{
    "detail": "Tag not found"
}

"""
