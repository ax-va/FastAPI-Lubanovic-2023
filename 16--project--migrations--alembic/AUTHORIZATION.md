# Authorization

## Access Levels

| Role   | Description                                     |
|--------|-------------------------------------------------|
| Public | Endpoint is available without authentication    |
| User   | Endpoint requires an authenticated user         |
| Admin  | Endpoint requires an uthenticated administrator |

## Access Matrix

| Endpoint                                              | Description                                  | Public | User | Admin |
|-------------------------------------------------------|----------------------------------------------|:------:|:----:|:-----:|
| POST /token                                           | Obtain an access token (JWT)                 |   ✅    |  ✅   |   ✅   |
| POST /users                                           | Register a new user                          |   ✅    |  ❌   |   ❌   |
| GET /users/me                                         | Get information about the authenticated user |   ❌    |  ✅   |   ✅   |
| DELETE /users/me                                      | Delete the authenticated user's account      |   ❌    |  ✅   |   ✅   |
| GET /users                                            | Get all users                                |   ❌    |  ❌   |   ✅   |
| GET /users/{id}                                       | Get a user by ID                             |   ❌    |  ❌   |   ✅   |
| GET /users?username={username}                        | Get a user by username                       |   ❌    |  ❌   |   ✅   |
| PUT /users/{id}                                       | Replace a user                               |   ❌    |  ❌   |   ✅   |
| PATCH /users/{id}/grant-admin                         | Grant administrator privileges               |   ❌    |  ❌   |   ✅   |
| PATCH /users/{id}/revoke-admin                        | Revoke administrator privileges              |   ❌    |  ❌   |   ✅   |
| DELETE /users/{id}                                    | Delete a user                                |   ❌    |  ❌   |   ✅   |
| GET /explorers                                        | Get all explorers                            |   ✅    |  ✅   |   ✅   |
| GET /explorers/{id}                                   | Get an explorer by ID                        |   ✅    |  ✅   |   ✅   |
| GET /explorers/{id}/creatures                         | Get all creatures bound to an explorer       |   ✅    |  ✅   |   ✅   |
| POST /explorers                                       | Create an explorer                           |   ❌    |  ✅   |   ✅   |
| POST /explorers/{explorer_id}/creatures/{creature_id} | Bind an explorer and a creature              |   ❌    |  ✅   |   ✅   |
| PUT /explorers/{id}                                   | Replace an explorer                          |   ❌    |  ✅   |   ✅   |
| DELETE /explorers/{id}                                | Delete an explorer                           |   ❌    |  ✅   |   ✅   |
| GET /creatures                                        | Get all creatures                            |   ✅    |  ✅   |   ✅   |
| GET /creatures/{id}                                   | Get a creature by ID                         |   ✅    |  ✅   |   ✅   |
| GET /creatures/{id}/explorers                         | Get all explorers bound to a creature        |   ✅    |  ✅   |   ✅   |
| POST /creatures                                       | Create a creature                            |   ❌    |  ✅   |   ✅   |
| POST /creatures/{creature_id}/explorers/{explorer_id} | Bind a creature and an explorer              |   ❌    |  ✅   |   ✅   |
| PUT /creatures/{id}                                   | Replace a creature                           |   ❌    |  ✅   |   ✅   |
| DELETE /creatures/{id}                                | Delete a creature                            |   ❌    |  ✅   |   ✅   |


