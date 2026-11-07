"""Διάλεξη 9: η Πυθία ως API. Το ticket γίνεται endpoint του FastAPI.

Χρήση:  uvicorn app:app --reload
        και στον browser: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pythia_ticket import Ticket, extract_ticket

app = FastAPI(title="Πυθία: email σε ticket")

class EmailIn(BaseModel):
    text: str

@app.post("/ticket", response_model=Ticket)
def make_ticket(email: EmailIn):
    try:
        ticket, _, _ = extract_ticket(email.text)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return ticket
