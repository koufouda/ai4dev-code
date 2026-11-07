"""Έλεγχος πριν από το μάθημα: κλειδιά, Ollama και μία δοκιμαστική κλήση σε κάθε μοντέλο.

Χρήση:  python check.py
"""
import os
import urllib.request

from dotenv import load_dotenv

load_dotenv()
from litellm import completion

def ok(msg):
    print("  [OK]       ", msg)

def bad(msg):
    print("  [ΠΡΟΣΟΧΗ]  ", msg)

print("Κλειδιά στο .env")
for key in ("GEMINI_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
    (ok if os.getenv(key) else bad)(f"{key}: {'υπάρχει' if os.getenv(key) else 'λείπει'}")

print("Ollama")
try:
    urllib.request.urlopen("http://localhost:11434", timeout=3)
    ok("τρέχει στο localhost:11434")
except Exception:
    bad("δεν απαντά: ανοίξτε την εφαρμογή Ollama")

print("Μοντέλα (μία μικρή κλήση στο καθένα)")
names = [os.getenv("MODEL"), os.getenv("MODEL_LOCAL"), *(os.getenv("ARENA_MODELS") or "").split(",")]
for model in sorted({n.strip() for n in names if n and n.strip()}):
    try:
        completion(model=model, messages=[{"role": "user", "content": "Πες μόνο: γεια"}], timeout=90)
        ok(model)
    except Exception as e:
        bad(f"{model}: {type(e).__name__}: {str(e).splitlines()[0][:110]}")
