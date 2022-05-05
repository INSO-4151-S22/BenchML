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
    timezone: str
    cors_allow_origins: str
    cors_allow_credentials: bool
    cors_allow_methods: str
    cors_allow_headers: str
    optimizer_resources: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
