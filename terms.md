#### RESTful (REST = Representational State Transfer)

- Usually uses HTTP 

- Client-server architecture

- Stateless (each request is independent)

- Server responses can be marked as cacheable

- Resource-based (resources identified by URIs)

- Uniform interface (standard HTTP methods such as GET, POST, PUT, PATCH, DELETE)

- Layered system (intermediaries may exist between client and server)

#### Three-tier model

- Presentation Layer (e.g., by using React)

- Business Logic Layer (e.g., by using FastAPI)

- Data Layer (e.g., by using PostgreSQL)


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

*Dependency Injection* is a design pattern in which an object or function receives its dependencies from the outside instead of creating them itself.
Dependencies are injected, not installed.


