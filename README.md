# FastAPI-Web-Applications-2026

**FastAPI Web Applications** is a comprehensive educational repository dedicated to Python web development with FastAPI.
It provides both the theoretical background and a step-by-step implementation of a complete web application.

Throughout the project, new technologies and concepts are introduced incrementally, 
including Pydantic, Pytest, SQLAlchemy, SQLModel, asynchronous programming, and database migrations with Alembic.

The repository was originally created while studying 
the book *"FastAPI: Modern Python Web Development"* by Bill Lubanovic (O'Reilly Media, 2023).
During learning, however, the project evolved far beyond the original material.
The codebase has been substantially redesigned, and many essential topics have been
expanded into comprehensive chapters with detailed explanations 
that provide a deeper understanding of modern FastAPI application development.
You can think of this repository as **"Bill Lubanovic on steroids"**.

## Used Packages for Python 3.12.5

See `requirements.txt`.

### The FastAPI framework
```shell
$ pip install fastapi
```

### The Uvicorn ASGI server with dependencies written in C
```shell
$ pip install "uvicorn[standard]"
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
$ pip install httpx2
```

### Authentication

- JWT
    ```shell
    $ pip install python-jose[cryptography]
    ```

- Hashing and verifying passwords
    ```shell
    $ pip install pwdlib[argon2]
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

### Testing
```shell
$ pip install pytest
$ pip install pytest-mock
````

Run tests
```shell
$ pytest -v
```

### Property-Based Testing
```shell
$ pip install hypothesis
$ pip install schemathesis
```

### Relational Database

- SQLAlchemy

  ```shell
  $ pip install SQLAlchemy
  ```

- SQLModel

  ```shell
  $ pip install sqlmodel
  ```

### Async

- Async for SQLite
  ```shell
  $ pip install aiosqlite
  ```

- Async for Pytest
  ```shell
  $ pip install pytest-asyncio
  ```

### Alembic

```shell
$ pip install alembic
```
