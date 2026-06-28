#### RESTful (REST = Representational State Transfer)

- Usually uses HTTP 

- Client-server architecture

- Stateless (each request is independent)

- Server responses can be marked as cacheable

- Resource-based (resources identified by URIs)

- Uniform interface (standard HTTP methods such as `GET`, `POST`, `PUT`, `PATCH`, `DELETE`)

- Layered system (intermediaries may exist between client and server; it has nothing to do with the three-tier model)

#### Three-tier model

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

- `GET /users?sort=country`: Retrieve all users, sorted by country

- `GET /users?offset=10&size=10`: Retrieve users in places 10 through 19

- `GET /users?sort=country&offset=10&size=10`: Retrieve all users, sorted by country, in places 10 through 19

- `POST /users name="AxVa" country="DE"`: Create a new user

- `PUT /users/25`: Completely replace the user with ID 25

- `PATCH /uses/25`: Partially update the user with ID 25

- `DELETE /users/25`: Delete the user with ID 25
