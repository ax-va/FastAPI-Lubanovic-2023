#### REST = Representational State Transfer 

- REST is s an architecture style for distributed systems, especially web APIs.
It is not a protocol, framework, or data format.

- Rest is usually implemented over HTTP, although it is not strictly tied to HTTP.

- A system is *RESTful* when it follows the REST architectural constraints:

  - *Client-Server*:

    The client and sever have separate responsibilities. 
    The client handles the user interface, while the server stores data and implements application logic.

  - *Stateless*:
    
    Every request must contain all information required to process it.
    The server does not rely on client session state stored between requests.

  - *Cacheable*:
    
    Server responses indicate whether they may be cached. 
    Caching can reduce server load and improve performance.

  - *Uniform Interface*:
    
    Clients interact with resources though a consistent interface. 
    This includes resources identified by URIs, representations of resources (commonly JSON), 
    self-described requests and responses, resource manipulation though representations,
    hypermedia links (when applicable).

  - *Layered System*:
    
    Intermediaries such as proxies, gateways, load balancers, and caches may exist between the client and the server.
    The client does not need to know whether it communicates directly with the final server.

  - *Code on Demand (optional)*:
    
    The server may send executable code to the client, such aas JavaScript.

#### RESTful API

A RESTful API is an API designed according to the REST architectural constraints.

#### HTTP = HyperText Transfer Protocol

- HTTP is an application-layer protocol.

- Defines how requests and responses are formatted and exchanged between a client and a server over a network.

- Although originally designed for transferring hypertext documents (HTML),
  HTTP is now used to transfer many types of data, including JSON, XML, images, audio, video, and files.

- HTTP is a stateless protocol: each request is independent and contains all information required to process it.

- HTTP runs over TCP. HTTPS runs over TLS over TCP.

#### TCP = Transmission Control Protocol

- TCP is a transport-layer protocol that provides reliable, ordered, and error-checked delivery of data between two hosts.

- TCP establishes a connection between the client and the server before exchanging data.

#### TLS = Transport Layer Security

- TLS is a cryptographic protocol that provides secure communication over a network.

#### HTTP vs HTTPS

- HTTP sends data in plain text: HTTP (Application Layer) → TCP (Transport Layer)

- HTTPS is simply HTTP running over a TLS-encrypted TCP connection: HTTP (Application Layer) → TLS → TCP (Transport Layer)

#### Layers and Protocols

| Layer       | Protocols    |
|-------------|--------------|
| Application | HTTP, HTTPS  |
| Security    | TLS          |
| Transport   | TCP          |
| Internet    | IP           |

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

### Data Layer

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

#### Repository Pattern

- The *Repository Pattern* is a design pattern that provides a layer between 
the business logic (service layer) and the data source.

- The repository encapsulates all data access logic and hides implementation details
of the underlying storage (e.g., SQLite, PostgreSQL, REST API, file system).

- The service works only with the repository interface and does not know where or how the data is stored.

- Benefits:
  - Separation of concerns.
  - Easier testing: the repository can be replaced with a fake and a mock.
  - The data source can be changed without modifying the business logic.
  - Works well with Dependency Injection.

- Example:
  ```
  Data Layer: Repository
    |-- SQLite
    |-- PostgreSQL
    |-- In-memory
    |-- Fake Repository
  ```

### Authentication and Authorization

#### Authentication: Who Are You?

- Authentication is the process of verifying a user's identity.

- A user provides credentials (such as a username and password), and the server verifies that they are valid.

- If the verification succeeds, the user is considered authenticated.

- Authentication verifies a user's identity before granting access to protected resources or allowing restricted actions.

Examples:

- *Username and password:* The user proves their identity by providing a username and password.


- *API key:* The client authenticates by sending a unique secret key with each request.


- *JSON Web Token (JWT):* A signed token format.

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

#### DDoS = Distributed Denial-of-Service

Distributed Denial-of-Service (DDoS) is an attack 
in which a large number of compromised computers or devices simultaneously send requests to a server.
The goal is to overwhelm the server's resources and make the service unavailable to legitimate users.

#### Middleware

*Middleware* is a component that intercepts HTTP requests and responses.
It runs before and after an endpoint, allowing cross-cutting functionality
such as logging, authentication, cross-origin resource sharing (CORS), compression, and request timing.
Unlike FastAPI's dependencies, FastAPI's middleware is typically applied to all requests in the application.

#### CORS = Cross-Origin Resource Sharing

*CORS* is browser security mechanism that controls 
whether a web page from one origin can access resources from another origin.
A server enables cross-origin access by sending CORS headers, 
such as `Acces-Control-Allow-Origin`.
CORS applies only to browsers and does not restrict server-to-server requests or tolls like `curl` or Postman.

CORS protects the browser, not the API. 
JWT (or another authentication mechanism) protects the API by proving the client's identity.
They solve different security problems and are often used together.

### Testing

#### Monkeypatch

- Monkeypatch replaces a real object with another real object.

- Use it when the code should continue working normally, but with a different implementation
  (e.g., an in-memory SQLite database).

#### Mocker

- Mocker replaces an object with a `Mock`.

- Use it when you want to isolate the unit under test and verify interactions
  (`assert_called_once_with()`, `call_count`, `call_args`, etc.).


#### TestClient

*TestClient* allows testing a FastAPI application without starting a server or opening a real TCP connection.
HTTP requests are sent directly to the ASGI application in memory, making integration tests fast and isolated.

#### Property-Based Testing

Property-based testing complements traditional testing rather than replacing it.

  - *Unit tests* verify individual functions and components.

  - *Integration/API tests* verify specific business scenarios.

  - *Property-bases tests* automatically explore a large number of input combinations and edge cases.

Unlike conventional tests, *property-based testing* verifies general properties of a system
rather than a small set of manually chosen examples.
Test inputs are generated automatically, allowing many different cases to be explored with minimal test code.

- *Hypothesis*:
  
  - Hypothesis ia a property-based testing library for Python.
    Instead of specifying concrete input values, you define strategies that generate data automatically.
  
  - Hypothesis executes the test with many different inputs and, if a failure is found,
    reduces it to the smallest reproducible example (*shrinking*)

- *Schemathesis*:

  - Schemathesis applies property-based testing to REST APIs.
    
  - It reads the *OpenAPI* schema generated by FastAPI, automatically generates HTTP requests
    for all documented endpoints, and validates that responses conform to the API contract.

Hypothesis and Schemathesis understand only the properties or API contract you provide.
They do not understand business logic, so they may expose expected behavior 
if the testes property is formulated too broadly.
They are best used alongside conventional integration and API tests.
