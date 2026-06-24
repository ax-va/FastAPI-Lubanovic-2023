from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def greeting(request):
    return JSONResponse('Hello Starlette!')


app = Starlette(debug=True, routes=[
    Route('/hi', greeting),
])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("02-3--hello-starlette:app", reload=True)


"""
$ http localhost:8000/hi
HTTP/1.1 200 OK
content-length: 18
content-type: application/json
date: Wed, 24 Jun 2026 14:15:04 GMT
server: uvicorn

"Hello Starlette!"

"""
