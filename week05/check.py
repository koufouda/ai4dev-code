"""Έλεγχος πριν από τις διαλέξεις 9-10: πακέτα, κλειδιά, Ollama, και ένα δοκιμαστικό ticket.

Χρήση:  python check.py
"""
import os
import importlib
import urllib.request

for name in ["litellm", "dotenv", "pydantic", "fastapi", "uvicorn", "pytest"]:
    try:
        importlib.import_module(name)
        print("[OK]       πακέτο", name)
    except ImportError:
        print("[ΠΡΟΣΟΧΗ]  λείπει το πακέτο", name, "→ pip install -r requirements.txt")

from pythia_ticket import extract_ticket

for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"]:
    if os.getenv(key):
        print("[INFO]      " + key + ": υπάρχει")
    else:
        print("[INFO]      " + key + ": λείπει")

try:
    urllib.request.urlopen("http://localhost:11434", timeout=3)
    print("[OK]       Ollama στο localhost:11434")
except Exception:
    print("[ΠΡΟΣΟΧΗ]  το Ollama δεν απαντά: ανοίξτε την εφαρμογή Ollama")

text = "Η μηχανή καφέ βγάζει καπνό. Παραγγελία 12345. Γιώργος"
for model in [os.getenv("MODEL", "anthropic/claude-haiku-5-5"), os.getenv("MODEL_LOCAL", "ollama_chat/gemma3:4b")]:
    try:
        ticket, seconds, cost = extract_ticket(text, model=model)
        print(f"[OK]       {model}: {ticket.category} / {ticket.priority} / {ticket.order_number} ({seconds:.1f}s)")
    except Exception as e:
        print(f"[ΠΡΟΣΟΧΗ]  {model}: {type(e).__name__}: {str(e).splitlines()[0][:120]}")
