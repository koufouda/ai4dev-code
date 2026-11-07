"""Διάλεξη 23: το σύνολο δοκιμών ΠΑΝΩ στην εγκατεστημένη εφαρμογή. Σωστές απαντήσεις, χρόνος (p50, p95), σφάλματα.
Ό,τι μετρήσατε στο laptop, το ξαναμετράτε εκεί που θα τη χρησιμοποιήσουν: αλλάζουν δίκτυο, μνήμη, ρυθμίσεις.

Χρήση:  python remote_eval.py https://pythia.example.com
        python remote_eval.py http://localhost:8000 --min 0.7
(Αν η εφαρμογή έχει APP_TOKEN: πρώτα  $env:APP_TOKEN="..."  στο ίδιο terminal.)
"""
import sys
import os
import json
import time
import urllib.request
from pythia_tools import contains_all
from pythia_rag import option

url = sys.argv[1].rstrip("/") if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else sys.exit(__doc__)
minimum = float(option(sys.argv, "--min", 0.7))
cases = [c for c in json.load(open("tool_cases.json", encoding="utf-8")) if c["expect"]]
times, right, errors = [], 0, 0
for case in cases:
    req = urllib.request.Request(url + "/chat", data=json.dumps({"question": case["question"], "user_id": "remote-eval"}).encode(),
                                 headers={"Content-Type": "application/json", "X-Token": os.getenv("APP_TOKEN", "")})
    start = time.perf_counter()
    try:
        answer = json.load(urllib.request.urlopen(req, timeout=120))["answer"]
    except Exception as e:
        errors, answer = errors + 1, f"ΣΦΑΛΜΑ {type(e).__name__}: {e}"
    times.append(time.perf_counter() - start)
    ok = contains_all(answer, case["expect"])
    right += ok
    print(f"{'✓' if ok else '✗'} {times[-1]:5.1f}s  {case['question'][:45]:<46} {' '.join(answer.split())[:60]}")
times.sort()
score = right / len(cases)
print(f"\nΣωστά: {right}/{len(cases)} ({score:.0%}, όριο {minimum:.0%}) · σφάλματα: {errors} · p50 {times[len(times) // 2]:.1f}s · p95 {times[int(0.95 * (len(times) - 1))]:.1f}s")
sys.exit(1 if errors or score < minimum else 0)
