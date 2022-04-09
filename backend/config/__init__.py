from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    sqlalchemy_database_url: str 
    celery_broker_url: str
    celery_backend_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()