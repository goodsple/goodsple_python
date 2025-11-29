
from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'

    knowledge_id = Column(Integer, primary_key=True)
    knowledge_intent = Column(String(100), nullable=False)
    knowledge_question = Column(Text, nullable=False)
    knowledge_answer = Column(Text, nullable=False)
    knowledge_is_faq = Column(Boolean, default=False, nullable=False)
    knowledge_faq_category = Column(String(50))
    knowledge_is_active = Column(Boolean, default=True, nullable=False)
    knowledge_created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    knowledge_updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())