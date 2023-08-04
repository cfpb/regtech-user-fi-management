# User and Financial Institutions Management API
This app communicates with Keycloak to provide some user management functionality, as well as serving as `Institutions API` to retrieve information about institutions.

---
### Dependencies
- [Poetry](https://python-poetry.org/) is used as the package management tool. Once installed, just running `poetry install` in the root of the project should install all the dependencies needed by the app.
- [Docker](https://www.docker.com/) is used for local development where ancillary services will run.
- [jq](https://jqlang.github.io/jq/download/) is used for parsing API responses in the curl command examples shown below

---
## Pre-requesites
[SBL Project Repo](https://github.com/cfpb/sbl-project) contains the `docker-compose.yml` to run the ancillary services. 
- Not all services need to run, this module `regtech-user-fi-management` is part of the docker compose file, which doesn't need to be ran in docker for local development.
- Issuing `docker compose up -d pg keycloak` would start the necessary services (postgres, and keycloak)

---
## Running the app
Once the [Dependencies](#dependencies), and [Pre-requesites](#pre-requesites) have been satisfied, we can run the app by going into the `src` folder, then issue the poetry run command:
```bash
cd src
poetry run uvicorn main:app --reload --port 8888
```
### Local development notes
- [.env.template](.env.template) is added to allow VS Code to search the correct path for imports when writing tests, just copy the [.env.template](.env.template) file into `.env` file locally

---
## Retrieve credentials
Most of the functionalities provided in this module requires authentication, namely `Access Tokens`, these can be retrieved from Keycloak by simulating a login flow.
The Keycloak service should come pre-configured with 2 users:
- `user1` with the password `user`
- `admin1` with the password `admin`

To retrieve the an access token we can issue a curl command:
```bash
curl 'localhost:8880/realms/regtech/protocol/openid-connect/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=user1' \
--data-urlencode 'password=user' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'client_id=regtech-client' | jq -r '.access_token'
```

---
## Functionalities
There are 2 major functionalities provided by this app, one serves as the integration with Keycloak, and the other to integrate with Institutions database to show institutions' information. Below are the routers for these functionalities. As mentioned above, authentication is required to access the endpoints.
- The [admin](./src/routers/admin.py) router with `/v1/admin` path manages Keycloak integration, allow for things like update user information (i.e. First Name, Last Name), and associating with institutions
  - GET `/v1/admin/me` displays the current user's info based on the auth token provided
  - PUT `/v1/admin/me` allows for basic info update:
    ```json
    {
      "firstName": "Test",
      "lastName": "User"
    }
    ```
  - PUT `/v1/admin/me/institutions` allows for self association with institutions using LEI
    ```json
    ["TEST1LEI", "TEST2LEI"]
    ```
  - Full flow example from getting token to retrieving information about logged in user:
    ```bash
    export RT_ACCESS_TOKEN=$(curl 'localhost:8880/realms/regtech/protocol/openid-connect/token' \
    -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'username=user1' \
    --data-urlencode 'password=user' \
    --data-urlencode 'grant_type=password' \
    --data-urlencode 'client_id=regtech-client' | jq -r '.access_token')

    curl localhost:8888/v1/admin/me -H "Authorization: Bearer ${RT_ACCESS_TOKEN}" | jq -r '.'
    ```
- The [institutions](./src/routers/institutions.py) router with `/v1/institutions` path retrieves institutions information
  - GET `/v1/institutions` retrieves all institutions in the database
    - three accepted parameters allows for filtering and pagination:
      - `page`: page of the results, this is index based, so starts with `0`
      - `count`: the number of results per page, by default this is `100`
      - `domain`: the filter parameter to look for institutions with specified domain
  - POST `/v1/institutions` creates or updates an institution with its LEI as the key:
    ```json
    {
      "lei": "TESTBANK123",
      "name": "Test Bank 123"
    }
    ```
  - POST `/v1/institutions/{LEI}/domains` adds domains to the institution:
    ```json
    [
      {
        "domain": "test123.bank"
      },
      {
        "domain": "bank123.test"
      }
    ]
    ```
  - Full flow example from token retrieval to creating / updating an institution:
    ```bash
    export RT_ACCESS_TOKEN=$(curl 'localhost:8880/realms/regtech/protocol/openid-connect/token' \
    -X POST \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'username=admin1' \
    --data-urlencode 'password=admin' \
    --data-urlencode 'grant_type=password' \
    --data-urlencode 'client_id=regtech-client' | jq -r '.access_token')

    curl localhost:8888/v1/institutions/ -X POST \
    -H "Authorization: Bearer ${RT_ACCESS_TOKEN}" \
    -H 'Content-Type: application/json' \
    -d '{"lei": "TESTBANK123", "name": "Test Bank 123"}' | jq -r '.'
    ```
For both these routers, the needed roles to access each endpoint is decorated with the `@requires` decorator, i.e. `@requires(["query-groups", "manage-users"])`. Refer to [institutions router](./src/routers/institutions.py) for the decorator example; these roles corresponds to Keycloak's roles.

---
## API Documentation
This module uses the [FastAPI](https://fastapi.tiangolo.com/) framework, which affords us built-in [Swagger UI](https://swagger.io/tools/swagger-ui/), this can be accessed by going to `http://localhost:8888/docs`
- _Note_: The `Try It Out` feature does not work within the Swagger UI due to the use of `AuthenticationMiddleware`

---

## Open source licensing info

1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)