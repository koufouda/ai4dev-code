"""Διάλεξη 21: έχει ξεφύγει κάποιο κλειδί στον κώδικα; Ψάχνει μοτίβα κλειδιών σε όλα τα αρχεία κειμένου
(εκτός από το .env) και ελέγχει ότι το .env είναι στο .gitignore και στο .dockerignore.

Χρήση:  python secret_scan.py          (exit code 1 αν βρει κάτι: το CI σταματά)
"""
import os
import re
import sys

PATTERNS = [r"sk-ant-[A-Za-z0-9_\-]{20,}", r"sk-[A-Za-z0-9]{32,}", r"AIza[0-9A-Za-z_\-]{35}", r"api_key\s*=\s*['\"][^'\"]{16,}['\"]"]
SKIP_DIRS = {".git", ".venv", "__pycache__", "db", "logs", ".pytest_cache"}
found = []
for folder, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for name in files:
        if name == ".env":
            continue
        path = os.path.join(folder, name)
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in PATTERNS:
            for match in re.findall(pattern, text):
                found.append(f"{path}: {match[:8]}…")
for ignore_file in [".gitignore", ".dockerignore"]:
    if not os.path.exists(ignore_file) or ".env" not in open(ignore_file, encoding="utf-8").read().split():
        found.append(f"{ignore_file}: δεν περιέχει τη γραμμή .env")
print("\n".join(found) if found else "Κανένα κλειδί στον κώδικα, και το .env αγνοείται. ✓")
sys.exit(1 if found else 0)
