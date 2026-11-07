"""Διάλεξη 13: όλα τα έγγραφα του φακέλου docs/ → κομμάτια → embeddings → βάση (φάκελος db/).

Χρήση:  python ingest.py
        python ingest.py --size 500 --overlap 100
"""
import glob
import sys
import time
from pythia_rag import add_document, EMBED_MODEL, option

size = int(option(sys.argv, "--size", "800"))
overlap = int(option(sys.argv, "--overlap", "150"))
paths = sorted(glob.glob("docs/*.pdf") + glob.glob("docs/*.docx"))
paths = [p for p in paths if "~$" not in p]
start = time.perf_counter()
total = 0
for path in paths:
    n = add_document(path, size, overlap)
    total += n
    print(f"{n:>4} κομμάτια  {path}")
print(f"\nΣύνολο: {total} κομμάτια από {len(paths)} έγγραφα | {time.perf_counter() - start:.1f}s | {EMBED_MODEL}")
