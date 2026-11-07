"""Διάλεξη 13: η Πυθία ως API. Ανεβάζετε έγγραφο, ρωτάτε, παίρνετε απάντηση με πηγές.

Χρήση:  uvicorn app_rag:app --reload
        και στον browser: http://127.0.0.1:8000/docs
"""
import os
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from pythia_rag import add_document, load_index, search, answer, DOCS_DIR

app = FastAPI(title="Πυθία: ερωτήσεις στα έγγραφά σας")

class Question(BaseModel):
    question: str

@app.post("/upload")
def upload(file: UploadFile):
    name = os.path.basename(file.filename)
    if not name.lower().endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Μόνο αρχεία .pdf ή .docx")
    path = os.path.join(DOCS_DIR, name)
    with open(path, "wb") as f:
        f.write(file.file.read())
    chunks = add_document(path)
    if chunks == 0:
        raise HTTPException(status_code=422, detail="Δεν βρέθηκε κείμενο στο αρχείο (μήπως είναι σκαναρισμένο;)")
    return {"file": name, "chunks": chunks}

@app.post("/ask")
def ask(q: Question):
    index = load_index()
    if index is None:
        raise HTTPException(status_code=404, detail="Δεν υπάρχουν έγγραφα. Ανεβάστε πρώτα με το /upload.")
    results = search(index, q.question, "hybrid", 4)
    text, cost = answer(q.question, results)
    return {"answer": text, "sources": [f"{c['source']} ({c['place']})" for _, c in results], "cost": cost}
