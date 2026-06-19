from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict



class Settings(BaseSettings):
    DATABASE_URL: str

    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    
    REDIS_URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()