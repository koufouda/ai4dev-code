"""Διάλεξη 14: η ίδια ερώτηση με τρεις τρόπους αναζήτησης, δίπλα-δίπλα. Τρέξτε πρώτα το ingest.py.

Χρήση:  python compare.py "Τι σημαίνει το E05;"
        python compare.py "η καφετιέρα κάνει λίμνη από κάτω"
"""
import sys
from pythia_rag import load_index, search

query = sys.argv[1] if len(sys.argv) > 1 else "Τι σημαίνει το E05;"
index = load_index()
print(f"Ερώτηση: «{query}»")
for method in ["vector", "bm25", "hybrid"]:
    print(f"\n=== {method} ===")
    for score, c in search(index, query, method, 3):
        print(f"  {score:6.3f}  {c['source']} ({c['place']})  {c['text'][:60]}…")
