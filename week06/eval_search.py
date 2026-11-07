"""Διάλεξη 12: πόσο καλά βρίσκει η αναζήτηση τη σωστή απάντηση; Σκορ, όπως στη διάλεξη 10.

hit@1 = η σωστή απάντηση ήταν πρώτη. hit@3 = ήταν στις 3 πρώτες.

Χρήση:  python eval_search.py
        python eval_search.py --model openai/text-embedding-3-small
        python eval_search.py --model gemini/gemini-embedding-001
"""
import json
import sys
import time
from pythia_embed import EMBED_MODEL, embed, load_faq, faq_text, top_k, option

model = option(sys.argv, "--model", EMBED_MODEL)
cases = json.load(open("search_cases.json", encoding="utf-8"))
faq = load_faq()
start = time.perf_counter()
faq_vectors = embed([faq_text(item) for item in faq], model)
query_vectors = embed([case["query"] for case in cases], model)

hit1 = 0
hit3 = 0
print(f"{model} | {len(cases)} δοκιμές\n")
for case, vector in zip(cases, query_vectors):
    found = [item["id"] for _, item in top_k(vector, faq, faq_vectors, 3)]
    if found[0] == case["expected"]:
        hit1 += 1
    if case["expected"] in found:
        hit3 += 1
    mark = "✓" if found[0] == case["expected"] else ("~" if case["expected"] in found else "✗")
    print(f"{mark} {case['query'][:45]:<46} περίμενα {case['expected']}, βρήκε {found}")

print(f"\nhit@1: {hit1}/{len(cases)} | hit@3: {hit3}/{len(cases)} | {time.perf_counter() - start:.1f}s")
