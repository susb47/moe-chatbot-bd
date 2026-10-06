from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EduQ - MoE Bangladesh AI Assistant"
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()