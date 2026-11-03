from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    数据库会话依赖注入函数
    用于 FastAPI 的 Depends 注入，为每个请求提供独立的数据库会话
    请求结束后自动关闭会话释放连接
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
