"""Διάλεξη 16: cache απαντήσεων. Ίδια ερώτηση = καμία κλήση. Παρόμοια ερώτηση = ίσως καμία κλήση.

Χρήση:  python answer_cache.py                (αδειάζει την cache και κάνει τρεις ερωτήσεις)
"""
import os
import time
from pythia_rag import load_index
from pythia_arch import cache_get, cache_put, CACHE_FILE
from pythia_safe import ask_safe

if os.path.exists(CACHE_FILE):
    os.remove(CACHE_FILE)
index = load_index()
questions = ["Κάθε πότε κάνω αφαλάτωση στη ΜΠ-001;", "κάθε ποτε κανω αφαλατωση στη ΜΠ-001;", "Ανά πόσο καιρό χρειάζεται αφαλάτωση η μηχανή;"]
for q in questions:
    start = time.perf_counter()
    answer, kind = cache_get(q)
    cost = 0.0
    if answer is None:
        r = ask_safe(index, q)
        answer, cost = r["answer"], r["cost"]
        if r["found"]:
            cache_put(q, answer)
        kind = "miss → RAG"
    print(f"«{q}»\n   {kind} | {(time.perf_counter() - start) * 1000:.0f} ms | ${cost:.5f}\n   {answer[:90]}\n")
