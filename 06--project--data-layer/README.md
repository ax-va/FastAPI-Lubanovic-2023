# Data Layer

## Repository Pattern

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
