"""Έλεγχος πριν από τις διαλέξεις 17-18: πακέτα, Ollama, μοντέλο με εργαλεία, embeddings, βάση, αρχεία δεδομένων.

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
from pythia_tools import TOOLS

for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"]:
    print("[INFO]     " + key + (": υπάρχει" if os.getenv(key) else ": λείπει"))

try:
    urllib.request.urlopen("http://localhost:11434", timeout=3)
    print("[OK]       Ollama στο localhost:11434")
except Exception:
    print("[ΠΡΟΣΟΧΗ]  το Ollama δεν απαντά: ανοίξτε την εφαρμογή Ollama")

try:
    resp = completion(model=MODEL, messages=[{"role": "user", "content": "Πόσο κοστίζει η ΜΠ-001;"}], tools=TOOLS, num_retries=1)
    calls = [c.function.name for c in resp.choices[0].message.tool_calls or []]
    print(f"[OK]       {MODEL}: ζήτησε {calls}" if calls else f"[ΠΡΟΣΟΧΗ]  {MODEL}: απάντησε χωρίς εργαλείο")
except Exception as e:
    print(f"[ΠΡΟΣΟΧΗ]  {MODEL}: {type(e).__name__}: {str(e).splitlines()[0][:120]}")

try:
    print(f"[OK]       {EMBED_MODEL}: διάνυσμα {len(embed(['Καλημέρα'])[0])} αριθμών")
except Exception as e:
    print(f"[ΠΡΟΣΟΧΗ]  {EMBED_MODEL}: {type(e).__name__} → ollama pull embeddinggemma")

index = load_index()
print(f"[OK]       βάση db/: {len(index['chunks'])} κομμάτια" if index else "[ΠΡΟΣΟΧΗ]  η βάση είναι άδεια → python ingest.py")

for name in ["orders.json", "katalogos.txt", "emails.json", "tool_cases.json", "agent_cases.json"]:
    print(f"[OK]       {name}" if os.path.exists(name) else f"[ΠΡΟΣΟΧΗ]  λείπει το {name}: αποσυμπιέστε ξανά το Week09_code.zip")
