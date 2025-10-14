# app/api/chat.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List # List 타입을 import 합니다.

# 우리가 직접 만든 모듈들을 import 합니다.
from app.db.session import get_db
from app.schemas import chat_schema
from app.crud import crud_knowledge

# 'router'는 API 경로들을 그룹화하는 데 사용됩니다.
router = APIRouter()

# --- '새 지식 추가' API 엔드포인트 ---
@router.post(
    "/knowledge",
    response_model=chat_schema.KnowledgeBaseResponse,
    summary="새로운 지식 베이스 항목 추가",
    description="관리자 페이지에서 새로운 의도, 질문, 답변을 DB에 저장합니다."
)
async def create_new_knowledge(
        *,
        # Depends(get_db)는 이 API가 호출될 때마다 DB 세션을 자동으로 생성하고,
        # 작업이 끝나면 세션을 닫아주는 역할을 합니다.
        db: AsyncSession = Depends(get_db),

        # knowledge_in 변수는 HTTP 요청의 Body 부분을
        # KnowledgeBaseCreate 스키마에 맞춰 자동으로 검증하고 받아옵니다.
        knowledge_in: chat_schema.KnowledgeBaseCreate
):
    """
    새로운 지식 베이스 항목을 생성합니다.
    """
    # 1. crud 함수를 호출하여 DB에 데이터를 저장합니다.
    new_knowledge = await crud_knowledge.create_knowledge(db=db, knowledge_in=knowledge_in)

    # 2. 저장된 결과를 클라이언트에게 반환합니다.
    return new_knowledge

# (참고: 나중에 여기에 GET, PUT, DELETE 등 다른 API들을 추가하게 됩니다.)

# ▼▼▼▼▼ 이 API를 새로 추가해주세요 ▼▼▼▼▼
@router.get(
    "/knowledge",
    # 응답 모델은 'KnowledgeBaseResponse' 스키마의 '리스트' 형태가 될 것입니다.
    response_model=List[chat_schema.KnowledgeBaseResponse],
    summary="전체 지식 베이스 목록 조회",
    description="DB에 저장된 모든 지식 베이스 항목을 리스트 형태로 가져옵니다."
)
async def get_knowledge_list(
        *,
        db: AsyncSession = Depends(get_db)
):
    """
    전체 지식 베이스 목록을 조회합니다.
    """
    # 1. crud 함수를 호출하여 DB에서 모든 데이터를 가져옵니다.
    knowledge_list = await crud_knowledge.get_multi(db=db)

    # 2. 조회된 결과를 클라이언트에게 반환합니다.
    return knowledge_list