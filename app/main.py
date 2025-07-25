from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "GoodsPle Chatbot Server is running!"}