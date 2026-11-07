"""Έλεγχος πριν από τις διαλέξεις 13-14: πακέτα, Ollama, μοντέλα, έγγραφα.

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

from pythia_rag import MODEL, EMBED_MODEL, completion, embed, load_all

for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"]:
    print("[INFO]     " + key + (": υπάρχει" if os.getenv(key) else ": λείπει"))

try:
    urllib.request.urlopen("http://localhost:11434", timeout=3)
    print("[OK]       Ollama στο localhost:11434")
except Exception:
    print("[ΠΡΟΣΟΧΗ]  το Ollama δεν απαντά: ανοίξτε την εφαρμογή Ollama")

try:
    resp = completion(model=MODEL, messages=[{"role": "user", "content": "Πες μόνο: εντάξει"}], num_retries=1)
    print(f"[OK]       {MODEL}: {resp.choices[0].message.content.strip()[:30]}")
except Exception as e:
    print(f"[ΠΡΟΣΟΧΗ]  {MODEL}: {type(e).__name__}: {str(e).splitlines()[0][:120]}")

try:
    print(f"[OK]       {EMBED_MODEL}: διάνυσμα {len(embed(['Καλημέρα'])[0])} αριθμών")
except Exception as e:
    print(f"[ΠΡΟΣΟΧΗ]  {EMBED_MODEL}: {type(e).__name__} → ollama pull embeddinggemma")

try:
    chunks = load_all()
    print(f"[OK]       docs/: {len(chunks)} κομμάτια από {len({c['source'] for c in chunks})} έγγραφα")
except Exception as e:
    print(f"[ΠΡΟΣΟΧΗ]  docs/: {type(e).__name__}: {e}")
