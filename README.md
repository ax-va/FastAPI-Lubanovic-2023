# FastAPI-Lubanovic-2023

## Packages to use

### The FastAPI framework
```shell
$ pip install fastapi
```

### The Uvicorn ASGI server
```shell
$ pip install uvicorn
```

### The HTTPie command-line HTTP client
```shell
$ pip install httpie
```

Example: request `http://example.com/` and print (`-p`) request headers (`H`), request body (`B`), and response headers (`h`)
```shell
$ http -p HBh http://example.com/
GET / HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: example.com
User-Agent: HTTPie/3.2.4



HTTP/1.1 200 OK
Age: 8995
Allow: GET, HEAD
CF-RAY: a12c5cf9ac46606b-MUC
Connection: keep-alive
Content-Encoding: gzip
Content-Type: text/html
Date: Sun, 28 Jun 2026 11:31:05 GMT
Last-Modified: Sat, 27 Jun 2026 11:26:45 GMT
Server: cloudflare
Transfer-Encoding: chunked
cf-cache-status: HIT

```
Use `-b` (equivalent to `--body` or `-p b`) only for the response body.

### The Requests synchronous HTTP client package
```shell
$ pip install requests
```

### The HTTPX synchronous/asynchronous HTTP client package
```shell
$ pip install httpx
```

### Testing
```shell
$ pip install pytest
$ pip install pytest-mock
````

Run tests
```shell
$ pytest -v
```

### Authentication
```shell
$ pip install python-jose[cryptography]
$ pip install passlib
$ pip install python-multipart
```

### Security
```shell
$ pip install python-dotenv
```

Generate a secret key
```shell
$ python -c "import secrets; print(secrets.token_hex(32))"
b9f3f6a080cfc1fd67dfe1f6e9e6cd2f119d09d4a58884fa7c7ead61216873e9
```

Add ".env" to `.gitignore` and store the following in `.env`
```shell
JWT_SECRET_KEY=<secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```