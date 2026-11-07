"""Διάλεξη 14: αναζήτηση με λέξεις (BM25), και γιατί τα ελληνικά θέλουν κανονικοποίηση.

Χρήση:  python bm25_demo.py "ΕΓΓΥΗΣΗ μηχανης"
        python bm25_demo.py "E05"
"""
import sys
from pythia_rag import load_all, build_index, search_bm25, words

query = sys.argv[1] if len(sys.argv) > 1 else "ΕΓΓΥΗΣΗ μηχανης"
chunks = load_all()
print(f"Ερώτηση: «{query}»")
print("Λέξεις χωρίς κανονικοποίηση:", query.split())
print("Λέξεις με κανονικοποίηση:   ", words(query))

for stem in [False, True]:
    index = build_index(chunks, vectors=[], stem=stem)
    print(f"\n=== BM25 {'με' if stem else 'χωρίς'} κόψιμο λέξεων ===")
    for score, c in search_bm25(index, query, 3):
        print(f"  {score:5.2f}  {c['source']} ({c['place']})  {c['text'][:60]}…")
