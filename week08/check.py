"""Έλεγχος πριν από τις διαλέξεις 15-16: πακέτα, Ollama, μοντέλα, έγγραφα, βάση.

Χρήση:  python check.py
"""
import os
import importlib
import urllib.request

for name in ["litellm", "dotenv", "fastapi", "uvicorn", "multipart", "chromadb", "pymupdf", "docx", "rank_bm25"]:
    try:
        importlib.import_module(name)
        print("[OK]       πακέτο", name)
    except ImportError:
        print("[ΠΡΟΣΟΧΗ]  λείπει το πακέτο", name, "→ pip install -r requirements.txt")

from pythia_rag import MODEL, EMBED_MODEL, completion, embed, load_index
from pythia_arch import MODEL_LOCAL

for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"]:
    print("[INFO]     " + key + (": υπάρχει" if os.getenv(key) else ": λείπει"))

try:
    urllib.request.urlopen("http://localhost:11434", timeout=3)
    print("[OK]       Ollama στο localhost:11434")
except Exception:
    print("[ΠΡΟΣΟΧΗ]  το Ollama δεν απαντά: ανοίξτε την εφαρμογή Ollama")

for model in [MODEL, MODEL_LOCAL]:
    try:
        resp = completion(model=model, messages=[{"role": "user", "content": "Πες μόνο: εντάξει"}], num_retries=1)
        print(f"[OK]       {model}: {resp.choices[0].message.content.strip()[:30]}")
    except Exception as e:
        print(f"[ΠΡΟΣΟΧΗ]  {model}: {type(e).__name__}: {str(e).splitlines()[0][:120]}")

try:
    print(f"[OK]       {EMBED_MODEL}: διάνυσμα {len(embed(['Καλημέρα'])[0])} αριθμών")
except Exception as e:
    print(f"[ΠΡΟΣΟΧΗ]  {EMBED_MODEL}: {type(e).__name__} → ollama pull embeddinggemma")

index = load_index()
print(f"[OK]       βάση db/: {len(index['chunks'])} κομμάτια" if index else "[ΠΡΟΣΟΧΗ]  η βάση είναι άδεια → python ingest.py")
