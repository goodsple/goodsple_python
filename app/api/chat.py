# app/api/chat.py

from fastapi import APIRouter, Depends, HTTPException
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

# ▼▼▼▼▼ 이 두 개의 API를 새로 추가해주세요 ▼▼▼▼▼

# --- '지식 수정' API 엔드포인트 ---
@router.put(
    "/knowledge/{knowledge_id}",
    response_model=chat_schema.KnowledgeBaseResponse,
    summary="특정 지식 베이스 항목 수정"
)
async def update_knowledge(
        *,
        db: AsyncSession = Depends(get_db),
        knowledge_id: int, # URL 경로에서 ID를 받아옵니다.
        knowledge_in: chat_schema.KnowledgeBaseUpdate
):
    """
    ID로 특정 지식 항목을 찾아 내용을 수정합니다.
    """
    # 1. DB에서 해당 ID의 데이터를 찾습니다.
    existing_knowledge = await crud_knowledge.get(db=db, knowledge_id=knowledge_id)

    # 2. 데이터가 없으면 404 오류를 발생시킵니다.
    if not existing_knowledge:
        raise HTTPException(status_code=404, detail="해당 지식을 찾을 수 없습니다.")

    # 3. crud 함수를 호출하여 데이터를 수정합니다.
    updated_knowledge = await crud_knowledge.update(db=db, db_obj=existing_knowledge, obj_in=knowledge_in)
    return updated_knowledge

# --- '지식 삭제' API 엔드포인트 ---
@router.delete(
    "/knowledge/{knowledge_id}",
    response_model=chat_schema.KnowledgeBaseResponse,
    summary="특정 지식 베이스 항목 삭제"
)
async def delete_knowledge(
        *,
        db: AsyncSession = Depends(get_db),
        knowledge_id: int # URL 경로에서 ID를 받아옵니다.
):
    """
    ID로 특정 지식 항목을 찾아 삭제합니다.
    """
    # 1. DB에서 해당 ID의 데이터를 찾습니다. (수정 API와 동일)
    existing_knowledge = await crud_knowledge.get(db=db, knowledge_id=knowledge_id)

    # 2. 데이터가 없으면 404 오류를 발생시킵니다.
    if not existing_knowledge:
        raise HTTPException(status_code=404, detail="해당 지식을 찾을 수 없습니다.")

    # 3. crud 함수를 호출하여 데이터를 삭제합니다.
    deleted_knowledge = await crud_knowledge.remove(db=db, knowledge_id=knowledge_id)
    return deleted_knowledge

# --- 사용자 챗봇 대화 응답 API ---
@router.post(
    "/answer",
    response_model=chat_schema.ChatbotAnswerResponse,
    summary="사용자 질문에 대한 챗봇 답변 반환",
    description="프론트(또는 Spring)에서 사용자의 메시지를 전달하면, 적절한 의도(intent)와 답변을 반환합니다."
)
async def get_chatbot_answer(
        *,
        db: AsyncSession = Depends(get_db),
        user_input: chat_schema.ChatbotAnswerRequest
):
    """
    사용자의 질문을 분석하여 답변을 반환합니다.
    """
    try:
        # 1️⃣ Rasa 또는 규칙 기반 로직 호출 (현재는 임시 예시)
        # 실제 구현에서는 Rasa NLU 모델 또는 DB 기반 검색을 호출할 수 있음
        intent = "지도_사용법"
        confidence = 0.93
        answer_text = "지도를 움직여 원하는 지역으로 이동하면, 해당 지역에 등록된 굿즈들이 자동으로 표시됩니다."

        # 2️⃣ DB 로그 저장 (선택)
        # await crud_chatlog.create_log(db, user_input.text, intent, confidence, answer_text)

        # 3️⃣ 응답 반환
        return chat_schema.ChatbotAnswerResponse(
            answer=answer_text,
            intent=intent,
            confidence=confidence
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
