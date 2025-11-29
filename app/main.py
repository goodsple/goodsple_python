from fastapi import FastAPI
from app.api import chat

app = FastAPI(
    title="GoodsPle AI Chatbot Service",
    description="Rasa와 DB를 연동하여 챗봇 기능을 제공하는 API 서버입니다.",
    version="1.0.0"
)

app.include_router(chat.router, prefix="/api", tags=["KnowledgeBase"])

@app.get("/")
def read_root():
    return {"message": "GoodsPle AI Chatbot 서버가 실행 중입니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

# http://127.0.0.1:8000/docs