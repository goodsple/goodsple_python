from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. 비동기 엔진 생성
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# 2. 비동기 세션 메이커 생성 (1.4 버전용)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# 3. 요청마다 세션을 생성하고 닫는 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
