# # app/core/config.py
#
# from pydantic_settings import BaseSettings
#
# class Settings(BaseSettings):
#     # YAML 파일의 정보를 바탕으로 아래와 같이 수정합니다.
#     # 형식: postgresql+asyncpg://[유저명]:[비밀번호]@[호스트주소]:[포트]/[DB이름]
#     DATABASE_URL: str = "postgresql+asyncpg://goodsple:goodsple@54.180.142.86:5432/goodsple"
#
#     class Config:
#         # .env 파일을 사용하도록 설정 (보안을 위해 권장)
#         env_file = ".env"
#
# settings = Settings()

# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://goodsple:goodsple@54.180.142.86:5432/goodsple"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
