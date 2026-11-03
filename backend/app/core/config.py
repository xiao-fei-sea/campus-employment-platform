from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    应用配置类
    使用 Pydantic Settings 管理应用配置，支持环境变量覆盖默认配置
    """

    PROJECT_NAME: str = "高校就业服务平台"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    DATABASE_URL: str = "mysql+pymysql://root:107606@localhost:3306/campus_employment"
    REDIS_URL: str = "redis://localhost:6379/0"
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    OSS_ENDPOINT: Optional[str] = None
    OSS_ACCESS_KEY: Optional[str] = None
    OSS_SECRET_KEY: Optional[str] = None
    OSS_BUCKET_NAME: Optional[str] = None

    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: int = 587
    MAIL_SERVER: Optional[str] = None
    MAIL_FROM_NAME: str = "高校就业服务平台"

    LLM_API_KEY: Optional[str] = None
    LLM_API_BASE: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env" if os.path.exists(".env") else None
        case_sensitive = True


settings = Settings()
