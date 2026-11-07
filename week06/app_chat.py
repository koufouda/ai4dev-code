"""Διάλεξη 11: η Πυθία ως API συνομιλίας. Κάθε session έχει τη δική του μνήμη.

Χρήση:  uvicorn app_chat:app --reload
        και στον browser: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel
from pythia_memory import MODEL, SYSTEM, ask, window

app = FastAPI(title="Πυθία: συνομιλία με μνήμη")
sessions = {}

class ChatIn(BaseModel):
    session_id: str
    message: str

class ChatOut(BaseModel):
    answer: str
    input_tokens: int
    cost: float
    messages_in_memory: int

@app.post("/chat", response_model=ChatOut)
def chat(req: ChatIn):
    history = sessions.setdefault(req.session_id, [SYSTEM])
    history.append({"role": "user", "content": req.message})
    answer, numbers, _ = ask(window(history, 10), MODEL, "app_chat")
    history.append({"role": "assistant", "content": answer})
    return ChatOut(answer=answer, input_tokens=numbers["input"], cost=numbers["cost"], messages_in_memory=len(history))
