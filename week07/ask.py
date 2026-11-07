"""Διάλεξη 13-14: ρωτάτε, η Πυθία ψάχνει στα έγγραφα και απαντά. Τρέξτε πρώτα το ingest.py.

Χρήση:  python ask.py "Τι σημαίνει το σφάλμα E05;"
        python ask.py "…" --show                 (δείχνει και τα κομμάτια που βρήκε)
        python ask.py "…" --method vector        (vector, bm25 ή hybrid· προεπιλογή vector)
        python ask.py "…" --method hybrid --rerank
        python ask.py                            (ρωτά συνέχεια, «τέλος» για έξοδο)
"""
import sys
from pythia_rag import load_index, search, rerank, answer, option

method = option(sys.argv, "--method", "vector")
k = int(option(sys.argv, "--k", "4"))
index = load_index()
if index is None:
    sys.exit("Η βάση είναι άδεια. Τρέξτε πρώτα: python ingest.py")

def ask(question):
    cost = 0.0
    if "--rerank" in sys.argv:
        candidates = search(index, question, method, 10)
        results, rerank_cost = rerank(question, candidates, k)
        cost += rerank_cost
    else:
        results = search(index, question, method, k)
    if "--show" in sys.argv:
        for score, c in results:
            print(f"  {score:.3f}  {c['source']} ({c['place']})  {c['text'][:70]}…")
    text, answer_cost = answer(question, results)
    cost += answer_cost
    print(f"\nΠυθία: {text}\n   [{method}{' + rerank' if '--rerank' in sys.argv else ''} | k={k} | ${cost:.5f}]")

if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
    ask(sys.argv[1])
else:
    while True:
        question = input("\nΕρώτηση: ")
        if question == "τέλος":
            break
        ask(question)
