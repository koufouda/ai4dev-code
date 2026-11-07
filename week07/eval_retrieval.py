"""Διάλεξη 14: πόσο καλά βρίσκει η αναζήτηση το σωστό κομμάτι; hit@k και MRR στο rag_cases.json.

Φτιάχνει το ευρετήριο στη μνήμη, για να αλλάζετε μέθοδο, μέγεθος κομματιών και stemming χωρίς να πειράξετε τη βάση.

Χρήση:  python eval_retrieval.py                        (hybrid, k=4, κομμάτια 800)
        python eval_retrieval.py --method vector
        python eval_retrieval.py --method bm25 --no-stem
        python eval_retrieval.py --size 300
        python eval_retrieval.py --rerank               (hybrid + reranking: κάνει κλήσεις στο LLM)
        python eval_retrieval.py --all                  (vector, bm25, hybrid σε έναν πίνακα)
"""
import json
import sys
import time
from pythia_rag import load_all, embed, build_index, search, rerank, normalize, option

method = option(sys.argv, "--method", "hybrid")
k = int(option(sys.argv, "--k", "4"))
size = int(option(sys.argv, "--size", "800"))
overlap = int(option(sys.argv, "--overlap", "150"))
stem = "--no-stem" not in sys.argv
cases = json.load(open("rag_cases.json", encoding="utf-8"))
start = time.perf_counter()
chunks = load_all(size, overlap)
index = build_index(chunks, embed([c["text"] for c in chunks]), stem)
print(f"{len(chunks)} κομμάτια (size {size}, overlap {overlap}, stem {stem}) | ευρετήριο σε {time.perf_counter() - start:.1f}s\n")

def position(results, phrase):
    target = normalize(phrase)
    for i, (_, c) in enumerate(results, start=1):
        if target in normalize(c["text"]):
            return i
    return 0

def evaluate(method, use_rerank=False, verbose=True):
    hit1, hitk, mrr, cost = 0, 0, 0.0, 0.0
    for case in cases:
        if use_rerank:
            candidates = search(index, case["question"], method, 10)
            results, c = rerank(case["question"], candidates, k)
            cost += c
        else:
            results = search(index, case["question"], method, k)
        pos = position(results, case["must_contain"])
        hit1 += pos == 1
        hitk += pos > 0
        mrr += 1 / pos if pos else 0
        if verbose:
            mark = "✓" if pos == 1 else ("~" if pos else "✗")
            print(f"{mark} {pos or '-':>2}  {case['question'][:60]}")
    return hit1, hitk, mrr / len(cases), cost

if "--all" in sys.argv:
    print(f"{'μέθοδος':<10}{'hit@1':>8}{f'hit@{k}':>8}{'MRR':>8}")
    for m in ["vector", "bm25", "hybrid"]:
        h1, hk, score, _ = evaluate(m, verbose=False)
        print(f"{m:<10}{h1:>5}/{len(cases)}{hk:>5}/{len(cases)}{score:>8.2f}")
else:
    h1, hk, score, cost = evaluate(method, "--rerank" in sys.argv)
    print(f"\n{method}{' + rerank' if '--rerank' in sys.argv else ''} | hit@1 {h1}/{len(cases)} | hit@{k} {hk}/{len(cases)} | MRR {score:.2f} | ${cost:.4f} | {time.perf_counter() - start:.1f}s")
