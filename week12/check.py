"""Έλεγχος πριν από τις διαλέξεις 23-24: Python, πακέτα, Docker, git, κλειδί, Ollama, βάση, tests.

Χρήση:  python check.py
"""
import os
import sys
import shutil
import subprocess
import importlib
import urllib.request

def run(command):
    try:
        r = subprocess.run(command, capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace")
        return r.returncode == 0, (r.stdout or r.stderr).strip().splitlines()[-1:] or [""]
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, [type(e).__name__]

print(f"[OK]       Python {sys.version.split()[0]}")
for name in ["litellm", "dotenv", "fastapi", "uvicorn", "chromadb", "pymupdf", "docx", "rank_bm25", "pytest", "httpx"]:
    try:
        importlib.import_module(name)
        print("[OK]       πακέτο", name)
    except ImportError:
        print("[ΠΡΟΣΟΧΗ]  λείπει το", name, "→ pip install -r requirements.txt -r requirements-dev.txt")
ok, out = run(["docker", "info", "--format", "{{.ServerVersion}}"]) if shutil.which("docker") else (False, ["δεν βρέθηκε"])
print(f"[OK]       Docker {out[0]}" if ok else f"[ΠΡΟΣΟΧΗ]  Docker: {out[0] or 'δεν τρέχει'} → εγκαταστήστε/ανοίξτε το Docker Desktop")
ok, out = run(["git", "--version"]) if shutil.which("git") else (False, ["δεν βρέθηκε"])
print(f"[OK]       {out[0]}" if ok else "[ΠΡΟΣΟΧΗ]  git: δεν βρέθηκε → git-scm.com")
from pythia_rag import load_index
print("[INFO]     ANTHROPIC_API_KEY:", "υπάρχει" if os.getenv("ANTHROPIC_API_KEY") else "λείπει")
print("[INFO]     PSEUDO_SALT:", "υπάρχει" if os.getenv("PSEUDO_SALT") else "λείπει (η εφαρμογή χρησιμοποιεί προσωρινό· ορίστε το στο .env)")
try:
    urllib.request.urlopen("http://localhost:11434", timeout=3)
    print("[OK]       Ollama στο localhost:11434")
except OSError:
    print("[ΠΡΟΣΟΧΗ]  το Ollama δεν απαντά: ανοίξτε την εφαρμογή Ollama")
index = load_index()
print(f"[OK]       βάση db/: {len(index['chunks'])} κομμάτια" if index else "[ΠΡΟΣΟΧΗ]  η βάση είναι άδεια → python ingest.py (πριν από το docker build)")
ok, out = run([sys.executable, "secret_scan.py"])
print(f"[OK]       {out[0]}" if ok else f"[ΠΡΟΣΟΧΗ]  secret_scan: {out[0]}")
ok, out = run([sys.executable, "-m", "pytest", "-q"])
print(f"[OK]       pytest: {out[0]}" if ok else f"[ΠΡΟΣΟΧΗ]  pytest: {out[0]} → pytest -v")
