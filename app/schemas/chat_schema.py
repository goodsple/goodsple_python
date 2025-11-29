
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class KnowledgeBaseCreate(BaseModel):
    knowledge_intent: str
    knowledge_question: str
    knowledge_answer: str

class KnowledgeBaseUpdate(BaseModel):
    knowledge_intent: Optional[str] = None
    knowledge_question: Optional[str] = None
    knowledge_answer: Optional[str] = None
    knowledge_is_faq: Optional[bool] = None
    knowledge_is_active: Optional[bool] = None

class KnowledgeBaseResponse(BaseModel):
    knowledge_id: int
    knowledge_intent: str
    knowledge_question: str
    knowledge_answer: str
    knowledge_is_faq: bool
    knowledge_is_active: bool
    knowledge_created_at: datetime
    knowledge_updated_at: datetime

    class Config:
        orm_mode = True


class ChatbotAnswerRequest(BaseModel):
    text: str


class ChatbotAnswerResponse(BaseModel):
    answer: str
    intent: str
    confidence: float