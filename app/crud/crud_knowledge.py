# app/crud/crud_knowledge.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge import KnowledgeBase
from app.schemas.chat_schema import KnowledgeBaseCreate # 아직 만들지 않았지만 곧 만들 파일입니다.

async def create_knowledge(db: AsyncSession, *, knowledge_in: KnowledgeBaseCreate) -> KnowledgeBase:
    """
    DB에 새로운 지식 항목을 추가합니다.
    """
    # 1. Pydantic 모델로 받은 데이터를 SQLAlchemy 모델 객체로 변환합니다.
    db_obj = KnowledgeBase(
        knowledge_intent=knowledge_in.knowledge_intent,
        knowledge_question=knowledge_in.knowledge_question,
        knowledge_answer=knowledge_in.knowledge_answer
    )
    # 2. 세션에 객체를 추가합니다. (아직 DB에 저장된 것은 아님)
    db.add(db_obj)
    # 3. 변경사항을 DB에 커밋(저장)합니다.
    await db.commit()
    # 4. DB에 저장된 객체를 다시 읽어와서 반환합니다. (ID 등 자동 생성된 값을 포함)
    await db.refresh(db_obj)
    return db_obj