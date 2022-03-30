# BenchML API

## Requirements
- PostgreSQL
- Redis

## Initial Setup
- Go to the file **config/database.py** and include the database url in the following variable **SQLALCHEMY_DATABASE_URL**. It should be in the following format: *`"postgresql://<user>:<password>@<server url>:<port>/<database>"`*
- Go to the file **controllers/tasks.py** and include the database url as value of the parameter **backend** and the redis database url as value of the parameter **broker**, both inside the class Celery. 
    - **backend** format: *`"db+postgresql://<user>:<password>@<server url>:<port>/<database>"`*
    - **broker** format: *`"redis://<server url>:<port>/0"`*

### Running the project
This project was built using FastAPI (https://fastapi.tiangolo.com/), a web framework built in Python. In order to run the project, we need to perform the following:
- Run the server: Uvicorn (https://www.uvicorn.org/)
    - ```uvicorn backend.main:app```
- Run the Distributed Task Queue: Celery (https://docs.celeryq.dev/)
    - ```celery -A backend.controller.tasks.celery worker```

## Documentation
- The **documentation/structure.sql** file includes the scripts needed to recreate the database.
- You might visit **`<url>/docs`** in your browser to test the API online.