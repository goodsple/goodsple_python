# app/crud/crud_knowledge.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.knowledge import KnowledgeBase
from sqlalchemy.future import select  # select 함수를 import 합니다.
from typing import List            # List 타입을 import 합니다.
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

# ▼▼▼▼▼ 이 함수를 새로 추가해주세요 ▼▼▼▼▼
async def get_multi(db: AsyncSession) -> List[KnowledgeBase]:
    """
    DB에서 모든 지식 항목을 조회합니다.
    """
    # 1. 'knowledge_base' 테이블의 모든 데이터를 조회하는 쿼리를 작성합니다.
    #    최신 항목이 위로 오도록 ID 기준 내림차순으로 정렬합니다.
    query = select(KnowledgeBase).order_by(KnowledgeBase.knowledge_id.desc())

    # 2. 쿼리를 실행하여 결과(result)를 받아옵니다.
    result = await db.execute(query)

    # 3. 결과에서 실제 데이터(SQLAlchemy 모델 객체)만 추출하여 리스트로 반환합니다.
    return result.scalars().all()