from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str

    jwt_secret_key: str

    minio_user: str
    minio_password: str

    alpha_vantage_api_key: str
    alpha_vantage_url: str
    request_timeout: int = 5

    class Config:
        env_file = ".env"

settings = Settings()