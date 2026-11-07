"""Διάλεξη 15: ελέγχει έγγραφα για κρυφές εντολές (prompt injection) πριν μπουν στη βάση.

Χρήση:  python scan_docs.py                  (docs/ και docs_attack/)
        python scan_docs.py docs_attack
"""
import glob
import os
import sys
from pythia_rag import load_chunks
from pythia_safe import scan_text

folders = sys.argv[1:] if len(sys.argv) > 1 else ["docs", "docs_attack"]
for folder in folders:
    for path in sorted(glob.glob(os.path.join(folder, "*.pdf")) + glob.glob(os.path.join(folder, "*.docx"))):
        chunks = load_chunks(path)
        flagged = [(c, scan_text(c["text"])) for c in chunks if scan_text(c["text"])]
        print(f"{'⚠' if flagged else '✓'} {path}: {len(chunks)} κομμάτια, {len(flagged)} ύποπτα")
        for c, patterns in flagged:
            print(f"     {c['place']}: {patterns}\n     «{c['text'][:160]}…»")
