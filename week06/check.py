"""Έλεγχος πριν από τις διαλέξεις 11-12: πακέτα, κλειδιά, Ollama, μοντέλα και embeddings.

Χρήση:  python check.py
"""
import os
import importlib
import urllib.request

for name in ["litellm", "dotenv", "fastapi", "uvicorn", "chromadb", "numpy", "matplotlib"]:
    try:
        importlib.import_module(name)
        print("[OK]       πακέτο", name)
    except ImportError:
        print("[ΠΡΟΣΟΧΗ]  λείπει το πακέτο", name, "→ pip install -r requirements.txt")

from pythia_memory import MODEL, MODEL_LOCAL, ask, count
from pythia_embed import EMBED_MODEL, embed

for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"]:
    print("[INFO]     " + key + (": υπάρχει" if os.getenv(key) else ": λείπει"))

try:
    urllib.request.urlopen("http://localhost:11434", timeout=3)
    print("[OK]       Ollama στο localhost:11434")
except Exception:
    print("[ΠΡΟΣΟΧΗ]  το Ollama δεν απαντά: ανοίξτε την εφαρμογή Ollama")

for model in [MODEL, MODEL_LOCAL]:
    try:
        answer, numbers, seconds = ask([{"role": "user", "content": "Πες μόνο: εντάξει"}], model, "check")
        print(f"[OK]       {model}: {answer.strip()[:30]} ({seconds:.1f}s, ${numbers['cost']:.6f})")
    except Exception as e:
        print(f"[ΠΡΟΣΟΧΗ]  {model}: {type(e).__name__}: {str(e).splitlines()[0][:120]}")

try:
    vectors = embed(["Καλημέρα"])
    print(f"[OK]       {EMBED_MODEL}: διάνυσμα {len(vectors[0])} αριθμών")
except Exception as e:
    print(f"[ΠΡΟΣΟΧΗ]  {EMBED_MODEL}: {type(e).__name__}: {str(e).splitlines()[0][:120]} → ollama pull embeddinggemma")

print(f"[INFO]     katalogos.txt: περίπου {count([{'role': 'user', 'content': open('katalogos.txt', encoding='utf-8').read()}])} tokens")
