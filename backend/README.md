# BenchML API

## Requirements
- PostgreSQL
- Redis
- Auth0 Account

## Initial Setup
### Environment Variables
Copy **.env.example** file into a new file called **.env**, which will contain the values of the env variables used by the backend. Please, include the corresponding values for the following:
- SQLALCHEMY_DATABASE_URL
    - This project uses Postgres as main database. This value should be in the following format: *`"postgresql://<user>:<password>@<server url>:<port>/<database>"`*
- CELERY_BROKER_URL
    - This project uses Redis as a broker. This value should be in the following format: *`"redis://<server url>:<port>/0"`*.
- CELERY_BACKEND_URL
    - This project uses Postgres as a broker. This value should be in the following format: *`"db+postgresql://<user>:<password>@<server url>:<port>/<database>"`*

- AUTH0_DOMAIN
    - This value is obtained through Auth0 dashboard in **Applications -> API**.
- AUTH0_API_AUDIENCE
    - This value is obtained through Auth0 dashboard in **Applications -> API**.
- AUTH0_ALGORITHMS
    - This value is obtained through Auth0 dashboard in **Applications -> API**.
- AUTH0_ISSUER
    - This value is obtained through Auth0 dashboard in **Applications -> API**.

> **_NOTE:_** SQLALCHEMY_DATABASE_URL and CELERY_BACKEND_URL should be connected to the same database.

### Running the project
This project was built using FastAPI (https://fastapi.tiangolo.com/), a web framework built in Python. In order to run the project, we need to perform the following:
- Run the server: Uvicorn (https://www.uvicorn.org/)
    - ```uvicorn main:app```
- Run the Distributed Task Queue: Celery (https://docs.celeryq.dev/)
    - ```celery -A controller.tasks.celery worker```

## Documentation
- The **documentation/structure.sql** file includes the scripts needed to recreate the database.
- You might visit **`<url>/docs`** in your browser to test the API online.