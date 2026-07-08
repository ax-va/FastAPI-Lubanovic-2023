#### RESTful (REST = Representational State Transfer)

- Usually uses HTTP 

- Client-server architecture

- Stateless (each request is independent)

- Server responses can be marked as cacheable

- Resource-based (resources identified by URIs)

- Uniform interface (standard HTTP methods such as `GET`, `POST`, `PUT`, `PATCH`, `DELETE`)

- Layered system (intermediaries may exist between client and server; it has nothing to do with the three-tier model)

#### Three-Tier Model

- Presentation Layer / Web Layer (FastAPI)

- Business Logic Layer / Service Layer

- Data Layer (SQLAlchemy or SQLModel) ↔ Database (PostgreSQL)

#### Server Gateway Interface

- WSGI = Web Server Gateway Interface

    - Python standard for communication between web servers and web applications

    - Synchronous (one request per worker at a time)

    - Used by frameworks such as Django and Flask

    - Example: Browser ↔ Nginx (web server) ↔ Gunicorn (WSGI server) ↔ Flask App (web application)
  
    - https://wsgi.readthedocs.io/en/latest/

- ASGI = Asynchronous Sever Gateway Interface

    - Successor to WSGI

    - Support `async` / `await`

    - Handles many concurrent connections efficiently
  
    - Used by FastAPI and Starlette
  
    - Example: Browser ↔ Nginx (web server) ↔ Uvicorn (ASGI server) ↔ FastAPI App (web application)
  
    - https://asgi.readthedocs.io/en/latest/

#### Dependency Injection (DI)

- *Dependency Injection* is a design pattern in which an object or function receives its dependencies from the outside 
instead of creating them itself.

- Dependencies are injected, not instantiated.

- FastAPI implements DI with `Depends()`: 
dependency functions are called automatically when your path operation function is called,
and they (dependency functions) return values are injected into your path operation function.
`Depends()` only tells FastAPI where that value comes from.

- FastAPI's dependency injection is more than just passing objects. 
Dependency functions benefit from the same automatic validation, type conversion,
and documentation generation as path operation functions.

- In FastAPI, there are dependencies on three levels: endpoint, router, and application.

#### HTTP Methods (Verbs)

- `GET`: Retrieve a resource

- `POST`: Create a new resource, or trigger an action or operation (e.g., login, logout, checkout, send-email, calculate)

- `PUT`: Completely replace a resource

- `PATCH`: Partially update a resource

- `DELETE`: Delete a resource

Examples:

- `GET /users`: Retrieve all users

- `GET /users/25`: Retrieve the user with ID 25 

- If the user with ID 25 was not found, the server returns `404 Not Found`

- `GET /users?sort=country`: Retrieve all users, sorted by country

- `GET /users?offset=10&size=10`: Retrieve users in places 10 through 19

- `GET /users?sort=country&offset=10&size=10`: Retrieve all users, sorted by country, in places 10 through 19

- `POST /users name="AxVa" country="DE"`: Create a new user

- `PUT /users/25 name="ax-va" country="DE"`: Completely replace the user with ID 25

- `PATCH /uses/25 country="US"`: Partially update the user with ID 25

- `DELETE /users/25`: Delete the user with ID 25

#### DB-API

Python DB-API is a standard interface between Python code and relational database drivers.

It defines common objects and methods such as:

- `connection` 
- `cursor`
- `execute()`
- `fetchone()`: Returns one tuple or `None`
- `fetchall()`: Returns a sequence of tuples
- `fetchmany(num)`: Returns up to `num` tuples
- `commit()`
- `rollback()`
- `close()`

DB-API does not standardize placeholder syntax. 
Each database driver defines its own parameter style 
(qmark: `?`; format: `%s`; numeric: `:<tuple_index>`; named: `:<dict_key>`; pyformat: `%(<dict_key>)s`), 
but all support parameterized queries.
Never insert user input into SQL using f-strings, `%`-string formatting, or string concatenation.
Always use parameterized queries.
SQL and parameter values are sent separately, so user input is treated as data 
rather than executable SQL code, preventing SQL injection.

Example:  
  ```python
  import psycopg
  
  conn = psycopg.connect(f"dbname=...")
  cursor = conn.cursor()
  
  cursor.execute(
    "SELECT * FROM creatures WHERE id = %s", 
    (creature_id,),
  )
  row = cursor.fetchone()

  cursor.execute(
    "UPDATE creatures SET country = %s WHERE id = %s", 
    ("Germany", 1),
  )
  conn.commit()

  cursor.close()
  conn.close()
  ```

Database drivers like sqlite3 (SQLite), psycopg (PostgreSQL), PyMySQL (MySQL), and mariadb (MariaDB) implement DB-API.

SQLAlchemy works on top of DB-API drivers.

#### Authentication: Who Are You?

- Authentication is the process of verifying a user's identity.

- A user provides credentials (such as a username and password), and the server verifies that they are valid.

- If the verification succeeds, the user is considered authenticated.

- Authentication verifies a user's identity before granting access to protected resources or allowing restricted actions.

Examples:

- *Username and password:* The user proves their identity by providing a username and password.


- *API key:* The client authenticates by sending a unique secret key with each request.


- *JSON Web Token (JWT):* A signed token format:

  - The JWT format consists of three parts: a header, a payload, and a signature.
  
  - The *header* contains metadata, such as the signing algorithm (`alg`) and token type (`typ`):
    ```json
    {
      "alg": "HS256",
      "typ": "JWT"
    }
    ```

  - The *payload* contains *claims*. 
    The claims describe the authenticated user or client inside a JWT payload, 
    such as their identifier (`sub`), expiration time (`exp`), issuer (`iss`) 
    or application-specific data like roles and permissions:
    ```json
    {
      "sub": "alice",
      "role": "admin",
      "exp": 1751914800
    } 
    ```
  - The *signature* verifies that the token has not been modified and was signed by a trusted issuer.

  - The header and payload are Base64URL-encoded. A signature is then generated from them using the selected algorithm
    and a *secret key*. Finally, the there parts are joined with dots (`header.payload.signature`) to form the JWT,
    which is sent in the `Authorization: Bearer <token>` header.

  - JWT is typically issued after authentication and sent with subsequent requests instead of the user's credentials.

  - JWT is not part of *OAuth2*, but it is a widely used token format for OAuth2 access tokens.


- *Bearer Token*: An HTTP authentication scheme in which the client sends an access token in the `Authorization` header:
  ```
  Authorization: Bearer <token>
  ```
  The word *Bearer* means *the bearer (holder) of the token*. 
  Anyone who presents a valid Bearer token is considered authenticated.
  A Bearer token is often a JWT, but it can also be an opaque token.


- *OAuth2:* OAuth 2.0 (*Open Authorization*) is an authorization framework.

  - Authentication identifies the user, while OAuth2 defines how access tokens are obtained and used to access protected resources.
    After a user is authenticated, the server issues an access token instead of requiring the user's credentials for every request.

  - OAuth2 does **not** define the format of an access token. The token may be a JWT or an opaque token.

  - OAuth2 is widely used for securing REST APIs, 
    delegated authorization with *OpenID Connect* ("Sign in with Google", "Sign in with GitHub"),
    or issuing and validating access tokens.
  
  - *OAuth 2.1* is a simplified and more secure revision of OAuth 2.0 
    that removes deprecated features and follows current security best practices. 

#### Authorization: What Are You Allowed To Do?

- Authorization is the process of determining what an authenticated user is allowed to do.

- After authentication,  the server checks the user's permissions or roles before allowing access to a resource or operation.

- If the user does not have sufficient permissions, the server returns `403 Forbidden`.

#### FastAPI Security

https://fastapi.tiangolo.com/tutorial/security/

#### Distributed Denial-of-Service (DDoS)

Distributed Denial-of-Service (DDoS) is an attack 
in which a large number of compromised computers or devices simultaneously send requests to a server.
The goal is to overwhelm the server's resources and make the service unavailable to legitimate users.
