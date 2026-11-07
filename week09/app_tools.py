"""Διάλεξη 17: η Πυθία με εργαλεία ως API. Η απάντηση δείχνει και ποια εργαλεία κλήθηκαν.

Χρήση:  uvicorn app_tools:app --reload
        και στον browser: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel
from pythia_tools import chat_with_tools

app = FastAPI(title="Πυθία με εργαλεία")

class Question(BaseModel):
    question: str

@app.post("/chat")
def chat(q: Question):
    answer, trace, cost = chat_with_tools(q.question)
    return {"answer": answer, "tools": [{"name": n, "arguments": a, "result": r[:200]} for n, a, r in trace], "cost": round(cost, 6)}
