"""Διάλεξη 14: reranking. Η αναζήτηση φέρνει 10 υποψήφια, ένα LLM τα ξαναβαθμολογεί.

Χρήση:  python rerank_demo.py "Μπορώ να επιστρέψω καφέ που άνοιξα;"
"""
import sys
from pythia_rag import load_index, search, rerank

query = sys.argv[1] if len(sys.argv) > 1 else "Μπορώ να επιστρέψω καφέ που άνοιξα;"
index = load_index()
candidates = search(index, query, "hybrid", 10)
print(f"Ερώτηση: «{query}»\n\n=== Πριν (hybrid, 10 πρώτα) ===")
for i, (score, c) in enumerate(candidates, 1):
    print(f"  {i:>2}. {c['source']} ({c['place']})  {c['text'][:60]}…")
results, cost = rerank(query, candidates, 3)
print(f"\n=== Μετά (reranking με LLM, 3 πρώτα) | ${cost:.5f} ===")
for score, c in results:
    print(f"  {score:>2}/10  {c['source']} ({c['place']})  {c['text'][:60]}…")
