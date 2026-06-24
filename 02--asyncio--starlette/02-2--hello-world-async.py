from fastapi import FastAPI
import asyncio

app = FastAPI()


@app.get("/hi")
async def greet():
    # `await` yields control back to the event loop,
    # allowing other coroutines to run
    # while the current coroutine is waiting.
    await asyncio.sleep(1)
    return "Hello World!"
    # FastAPI runs an async *event loop*
    # that coordinates the async path functions,
    # and a *threadpool* for synchronous path functions.


if __name__ == "__main__":
    import uvicorn
    # Don't need to run methods like `asyncio.gather` or `asyncio.run`
    uvicorn.run("02-2--hello-world-async:app", reload=True)

"""
$ http localhost:8000/hi
HTTP/1.1 200 OK
content-length: 14
content-type: application/json
date: Wed, 24 Jun 2026 14:03:05 GMT
server: uvicorn

"Hello World!"

"""
