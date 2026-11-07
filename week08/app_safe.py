"""Διάλεξη 15: η Πυθία ως API, με άμυνες. Έλεγχος εγγράφων στο ανέβασμα, παραπομπές και «δεν ξέρω» στην απάντηση.

Χρήση:  uvicorn app_safe:app --reload
        και στον browser: http://127.0.0.1:8000/docs
"""
import os
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from pythia_rag import add_document, load_chunks, load_index, DOCS_DIR
from pythia_safe import scan_text, ask_safe

app = FastAPI(title="Πυθία: απαντήσεις με παραπομπές και άμυνες")

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
    flagged = [c["place"] for c in load_chunks(path) if scan_text(c["text"])]
    if flagged:
        os.remove(path)
        raise HTTPException(status_code=422, detail=f"Το έγγραφο περιέχει κείμενο που μοιάζει με εντολές προς τον βοηθό ({', '.join(flagged)}). Δεν μπήκε στη βάση.")
    return {"file": name, "chunks": add_document(path)}

@app.post("/ask")
def ask(q: Question):
    index = load_index()
    if index is None:
        raise HTTPException(status_code=404, detail="Δεν υπάρχουν έγγραφα. Ανεβάστε πρώτα με το /upload.")
    return ask_safe(index, q.question)
