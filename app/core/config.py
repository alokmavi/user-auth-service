from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "User Auth Service"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = Field(default="super-secret-temporary-key-replace-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "user_auth_db"
    
    @property
    def DATABASE_URL(self) -> str:
        # Changed from postgresql:// to postgresql+psycopg://
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

app_settings = Settings()