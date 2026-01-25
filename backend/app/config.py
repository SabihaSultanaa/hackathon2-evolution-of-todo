from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    openai_api_key: str
    
    backend_url: str = "http://localhost:8000"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    app_title: str = "Todo API"
    app_version: str = "0.1.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

def get_settings():
    return Settings()