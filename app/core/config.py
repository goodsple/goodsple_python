# Pydantic v1 스타일
from pydantic import BaseSettings

class Settings(BaseSettings):
    # 필요시 .env로 덮어씀
    DATABASE_URL: str = "postgresql+asyncpg://goodsple:goodsple@54.180.142.86:5432/goodsple"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
