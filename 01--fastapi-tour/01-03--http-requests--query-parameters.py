from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def greet(who):
    return f"Hello {who}!"


# 1. Start Uvicorn internally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01-03--http-requests--query-parameters:app", reload=True)


# Or start Uvicorn externally with the command line
"""
$ uvicorn 01-03--http-requests--query-parameters:app --reload
"""
# and CTRL+C to shut down

# 2. Type in the browser
"""
localhost:8000/hi?who=AxVa
"""

# 3. Type the command line
"""
$ http -b localhost:8000/hi?who=ax-va
"Hello ax-va!"

$ http -b localhost:8000/hi who==Mom
"Hello Mom!"

"""

# 4. Type in the Python console
"""
>>> import requests
>>> r = requests.get("http://localhost:8000/hi?who=Mom")
>>> r.json()
'Hello Mom!'

>>> params = {"who": "Mom"}
>>> r = requests.get("http://localhost:8000/hi", params=params)
>>> r.json()
'Hello Mom!'

"""