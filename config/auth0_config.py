from functools import lru_cache

from pydantic import BaseSettings

class Settings(BaseSettings):
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ISSUER: str
    AUTH0_ALGORITHMS: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()