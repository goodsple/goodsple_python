# app/main.py

from fastapi import FastAPI
from app.api import chat  # 우리가 만든 chat.py를 import 합니다.

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="GoodsPle AI Chatbot Service",
    description="Rasa와 DB를 연동하여 챗봇 기능을 제공하는 API 서버입니다.",
    version="1.0.0"
)

# "/api" 라는 경로 아래에 chat.py에서 만든 모든 API를 포함시킵니다.
app.include_router(chat.router, prefix="/api", tags=["KnowledgeBase"])

# (참고: 나중에 다른 기능의 API 파일이 추가되면 여기에 계속 등록하면 됩니다.)
@app.get("/")
def read_root():
    return {"message": "GoodsPle AI Chatbot 서버가 실행 중입니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

# http://127.0.0.1:8000/docs