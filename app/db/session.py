# app/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# 1. 비동기 엔진 생성: 우리가 config.py에 설정한 DB URL을 사용합니다.
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 2. 비동기 세션 메이커 생성: DB와 통신할 때 사용할 세션을 만드는 공장입니다.
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# 3. API가 호출될 때마다 독립적인 DB 세션을 생성하고, 끝나면 닫아주는 함수입니다.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session