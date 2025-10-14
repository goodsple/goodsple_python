# app/models/knowledge.py

from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

# 모든 모델이 상속받을 기본 클래스
Base = declarative_base()

# 'knowledge_base' 테이블의 Python 버전 설계도
class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'  # 실제 DB 테이블 이름과 정확히 일치시켜야 합니다.

    knowledge_id = Column(Integer, primary_key=True)
    knowledge_intent = Column(String(100), nullable=False)
    knowledge_question = Column(Text, nullable=False)
    knowledge_answer = Column(Text, nullable=False)
    knowledge_is_faq = Column(Boolean, default=False, nullable=False)
    knowledge_faq_category = Column(String(50))
    knowledge_is_active = Column(Boolean, default=True, nullable=False)
    # tsvector 컬럼은 지금 당장 필요하지 않으므로 생략합니다.
    knowledge_created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    knowledge_updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())