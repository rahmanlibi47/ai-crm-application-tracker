from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict



class Settings(BaseSettings):
    APP_DATABASE_URL: str

    AUTH_SECRET_KEY: str
    SECRET_KEY: str
    AUTH_ALGORITHM: str
    
    REDIS_URL: str
    
    ADZUNA_APP_ID: str
    ADZUNA_APP_KEY: str
    ADZUNA_COUNTRY: str = "in"
    
    model_config = SettingsConfigDict(
        env_file=".env.docker"
    )


settings = Settings()