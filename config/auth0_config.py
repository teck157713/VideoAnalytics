from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ISSUER: str
    AUTH0_ALGORITHMS: str
    GITHUB_AUTH0_CLIENTID: str
    GITHUB_AUTH0_CLIENT_SECRET: str
    root_path: str = ""
    logging_level: str = "INFO"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()