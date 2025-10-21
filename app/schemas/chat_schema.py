# app/schemas/chat_schema.py


from pydantic import BaseModel, Field # Field를 import 합니다.
from typing import Optional
from datetime import datetime

# --- 지식 베이스(KnowledgeBase) 스키마 ---

# API가 '새 지식 추가' 요청을 받을 때의 데이터 모양 (Request Body)
class KnowledgeBaseCreate(BaseModel):
    knowledge_intent: str
    knowledge_question: str
    knowledge_answer: str

# ▼▼▼▼▼ 이 클래스를 새로 추가해주세요 ▼▼▼▼▼
class KnowledgeBaseUpdate(BaseModel):
    knowledge_intent: Optional[str] = None
    knowledge_question: Optional[str] = None
    knowledge_answer: Optional[str] = None
    knowledge_is_faq: Optional[bool] = None
    knowledge_is_active: Optional[bool] = None

# API가 클라이언트에게 '지식 정보'를 응답으로 보낼 때의 데이터 모양 (Response Body)
class KnowledgeBaseResponse(BaseModel):
    knowledge_id: int
    knowledge_intent: str
    knowledge_question: str
    knowledge_answer: str
    knowledge_is_faq: bool
    knowledge_is_active: bool
    knowledge_created_at: datetime
    knowledge_updated_at: datetime

    # 이 설정을 통해 SQLAlchemy 모델 객체를 Pydantic 모델로 자동 변환할 수 있습니다.
    class Config:
        orm_mode = True


# --- 사용자 챗봇 대화용 스키마 ---
class ChatbotAnswerRequest(BaseModel):
    text: str  # 사용자가 입력한 메시지


class ChatbotAnswerResponse(BaseModel):
    answer: str       # 챗봇의 답변 텍스트
    intent: str       # 의도(예: "지도_사용법")
    confidence: float # 신뢰도 (0.0 ~ 1.0)