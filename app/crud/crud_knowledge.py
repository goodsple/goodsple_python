# app/crud/crud_knowledge.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional, Dict, Any

from app.models.knowledge import KnowledgeBase
from app.schemas.chat_schema import KnowledgeBaseCreate, KnowledgeBaseUpdate

# --- Read (Single Item) ---
async def get(db: AsyncSession, knowledge_id: int) -> Optional[KnowledgeBase]:
    """ID로 특정 지식 항목 하나를 조회합니다."""
    result = await db.execute(select(KnowledgeBase).filter(KnowledgeBase.knowledge_id == knowledge_id))
    return result.scalars().first()

# --- Read (Multiple Items) ---
async def get_multi(db: AsyncSession) -> List[KnowledgeBase]:
    """모든 지식 항목을 조회합니다."""
    query = select(KnowledgeBase).order_by(KnowledgeBase.knowledge_id.desc())
    result = await db.execute(query)
    return result.scalars().all()

# --- Create ---
async def create_knowledge(db: AsyncSession, *, knowledge_in: KnowledgeBaseCreate) -> KnowledgeBase:
    """새로운 지식 항목을 추가합니다."""
    db_obj = KnowledgeBase(
        knowledge_intent=knowledge_in.knowledge_intent,
        knowledge_question=knowledge_in.knowledge_question,
        knowledge_answer=knowledge_in.knowledge_answer
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

# --- Update ---
async def update(db: AsyncSession, *, db_obj: KnowledgeBase, obj_in: KnowledgeBaseUpdate) -> KnowledgeBase:
    """기존 지식 항목을 수정합니다."""
    # Pydantic 모델을 dict로 변환
    update_data = obj_in.dict(exclude_unset=True)
    # dict의 각 항목을 SQLAlchemy 모델 객체의 속성으로 설정
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

# --- Delete ---
async def remove(db: AsyncSession, *, knowledge_id: int) -> Optional[KnowledgeBase]:
    """ID로 특정 지식 항목을 삭제합니다."""
    result = await db.execute(select(KnowledgeBase).filter(KnowledgeBase.knowledge_id == knowledge_id))
    db_obj = result.scalars().first()
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
    return db_obj