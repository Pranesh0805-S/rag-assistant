from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str
    claude_api_key: str = ""
    jwt_secret: str = "changeme"
    smtp_email: str
    smtp_password: str

    class Config:
        env_file = ".env"

settings = Settings()