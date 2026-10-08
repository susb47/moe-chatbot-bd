from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Changed from app_name to PROJECT_NAME to match your main.py
    PROJECT_NAME: str = "EduQ API" 
    gemini_api_key: str | None = None
    groq_api_key: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()