"""Εβδομάδα 11-12: η Πυθία έτοιμη για παραγωγή. Το API με εργαλεία της διάλεξης 17, συν:
/health για έλεγχο, δήλωση ότι ο χρήστης μιλά με AI, απόκρυψη προσωπικών δεδομένων, ψευδωνυμοποίηση,
και καταγραφή κάθε αιτήματος σε logs/ΕΕΕΕ-ΜΜ-ΗΗ.jsonl (μία γραμμή JSON ανά γεγονός).

Χρήση:  uvicorn app:app --reload               (στο laptop)
        docker compose up --build              (σε container, διάλεξη 21)
Νέο στη διάλεξη 23: αν οριστεί APP_TOKEN, το /chat θέλει την κεφαλίδα X-Token (μια δημόσια διεύθυνση = ο καθένας ξοδεύει τα λεφτά σας).
"""
import os
import json
import time
import uuid
import hashlib
import datetime
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from pythia_rag import MODEL
from pythia_tools import chat_with_tools
from pythia_arch import guard_input
from pythia_safe import output_guard

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
VERSION = os.getenv("APP_VERSION", "dev")
SALT = os.getenv("PSEUDO_SALT") or "dev-salt-ΑΛΛΑΞΤΕ-ΤΟ"
APP_TOKEN = os.getenv("APP_TOKEN", "")
DISCLOSURE = "Μιλάτε με ψηφιακό βοηθό (σύστημα AI). Οι απαντήσεις μπορεί να έχουν λάθη· για παραγγελίες και επιστροφές ισχύουν οι όροι του καταστήματος."

app = FastAPI(title="Πυθία", version=VERSION)

class Question(BaseModel):
    question: str
    user_id: str = "anonymous"

class Feedback(BaseModel):
    request_id: str
    good: bool

def pseudonym(user_id):
    return hashlib.sha256((SALT + user_id).encode()).hexdigest()[:16]

def log(event):
    now = datetime.datetime.now(datetime.timezone.utc)
    path = os.path.join(LOG_DIR, f"{now:%Y-%m-%d}.jsonl")
    line = json.dumps({"time": now.isoformat(timespec="seconds"), **event}, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    if os.getenv("LOG_STDOUT") == "1":
        print(line, flush=True)

@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION, "model": MODEL}

@app.post("/chat")
def chat(q: Question, x_token: str = Header(default="")):
    if APP_TOKEN and x_token != APP_TOKEN:
        raise HTTPException(status_code=401, detail="Λείπει ή είναι λάθος το X-Token.")
    request_id = uuid.uuid4().hex[:12]
    start = time.perf_counter()
    question, pii = guard_input(q.question)
    try:
        answer, trace, cost = chat_with_tools(question)
        error = None
    except Exception as e:
        answer, trace, cost = "Προσωρινό πρόβλημα. Δοκιμάστε ξανά σε λίγο.", [], 0.0
        error = f"{type(e).__name__}: {str(e)[:200]}"
    blocked = output_guard(answer)
    if blocked:
        answer = "Δεν μπορώ να απαντήσω σε αυτό. Επικοινωνήστε με την εξυπηρέτηση."
    log({"type": "chat", "request_id": request_id, "user": pseudonym(q.user_id), "question": question, "pii_masked": pii,
         "tools": [name for name, _, _ in trace], "answer": answer[:300], "blocked": blocked, "error": error,
         "cost": round(cost, 6), "ms": int((time.perf_counter() - start) * 1000), "model": MODEL, "version": VERSION})
    return {"request_id": request_id, "answer": answer, "disclosure": DISCLOSURE}

@app.post("/feedback")
def feedback(f: Feedback):
    log({"type": "feedback", "request_id": f.request_id, "good": f.good})
    return {"ok": True}
