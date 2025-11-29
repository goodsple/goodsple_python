from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.services.rasa_service import parse_intent

from app.db.session import get_db
from app.schemas import chat_schema
from app.crud import crud_knowledge

router = APIRouter()

@router.post(
    "/knowledge",
    response_model=chat_schema.KnowledgeBaseResponse,
    summary="새로운 지식 베이스 항목 추가",
    description="관리자 페이지에서 새로운 의도, 질문, 답변을 DB에 저장합니다."
)
async def create_new_knowledge(
        *,
        db: AsyncSession = Depends(get_db),

        knowledge_in: chat_schema.KnowledgeBaseCreate
):
    """
    새로운 지식 베이스 항목을 생성합니다.
    """
    new_knowledge = await crud_knowledge.create_knowledge(db=db, knowledge_in=knowledge_in)

    return new_knowledge

@router.get(
    "/knowledge",
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
    knowledge_list = await crud_knowledge.get_multi(db=db)

    return knowledge_list

@router.put(
    "/knowledge/{knowledge_id}",
    response_model=chat_schema.KnowledgeBaseResponse,
    summary="특정 지식 베이스 항목 수정"
)
async def update_knowledge(
        *,
        db: AsyncSession = Depends(get_db),
        knowledge_id: int,
        knowledge_in: chat_schema.KnowledgeBaseUpdate
):
    """
    ID로 특정 지식 항목을 찾아 내용을 수정합니다.
    """
    existing_knowledge = await crud_knowledge.get(db=db, knowledge_id=knowledge_id)

    if not existing_knowledge:
        raise HTTPException(status_code=404, detail="해당 지식을 찾을 수 없습니다.")

    updated_knowledge = await crud_knowledge.update(db=db, db_obj=existing_knowledge, obj_in=knowledge_in)
    return updated_knowledge

@router.delete(
    "/knowledge/{knowledge_id}",
    response_model=chat_schema.KnowledgeBaseResponse,
    summary="특정 지식 베이스 항목 삭제"
)
async def delete_knowledge(
        *,
        db: AsyncSession = Depends(get_db),
        knowledge_id: int
):
    """
    ID로 특정 지식 항목을 찾아 삭제합니다.
    """
    existing_knowledge = await crud_knowledge.get(db=db, knowledge_id=knowledge_id)

    if not existing_knowledge:
        raise HTTPException(status_code=404, detail="해당 지식을 찾을 수 없습니다.")

    deleted_knowledge = await crud_knowledge.remove(db=db, knowledge_id=knowledge_id)
    return deleted_knowledge

@router.post("/answer", response_model=chat_schema.ChatbotAnswerResponse)
async def get_chatbot_answer(*, db: AsyncSession = Depends(get_db),
                             user_input: chat_schema.ChatbotAnswerRequest):

    text = (user_input.text or "").strip()
    if not text:
        return chat_schema.ChatbotAnswerResponse(
            answer="질문 문장이 비었습니다. 내용을 입력해 주세요.",
            intent="input_empty",
            confidence=0.0
        )

    nlu = await parse_intent(text)
    intent = nlu.intent
    confidence = nlu.confidence

    THRESHOLD = 0.45
    if (not nlu.ok) or (confidence < THRESHOLD):
        return chat_schema.ChatbotAnswerResponse(
            answer="질문을 이해하지 못했습니다. 다른 표현으로 질문해 주세요.",
            intent="nlu_fallback",
            confidence=float(confidence)
        )

    kb_list = await crud_knowledge.get_multi(db=db)
    answer = next(
        (k.knowledge_answer for k in kb_list if k.knowledge_intent == intent and k.knowledge_is_active),
        None
    )

    if not answer:
        return chat_schema.ChatbotAnswerResponse(
            answer="해당 의도에 등록된 답변이 없습니다. 관리자에게 문의하세요.",
            intent=intent,
            confidence=float(confidence)
        )

    return chat_schema.ChatbotAnswerResponse(
        answer=answer,
        intent=intent,
        confidence=float(confidence)
    )