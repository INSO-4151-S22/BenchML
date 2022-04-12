from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    sqlalchemy_database_url: str 
    celery_broker_url: str
    celery_backend_url: str
    auth0_domain: str
    auth0_api_audience: str
    auth0_algorithms: str
    auth0_issuer: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
