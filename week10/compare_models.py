"""Διάλεξη 20: τα ίδια 16 τεστ σε όλα τα μοντέλα του models.txt. Ποσοστό σωστών ανά κατηγορία, χρόνος, κόστος.

model_cases.json: ελληνικά, JSON, ταξινόμηση, πράξη, «δεν ξέρω», εργαλεία.
Τα αποτελέσματα γράφονται και στο results.csv (για το compare_chart.py).

Χρήση:  python compare_models.py
        python compare_models.py ollama_chat/gemma3:4b anthropic/claude-haiku-5-5
"""
import sys
import json
import csv
from pythia_models import read_models, ask
from pythia_tools import TOOLS, contains_all

def correct(case, out):
    if "tool" in case:
        return out == case["tool"]
    if "json" in case:
        start, end = out.find("{"), out.rfind("}")
        try:
            data = json.loads(out[start:end + 1])
        except ValueError:
            return False
        if not all(k in data for k in case["json"]):
            return False
    return contains_all(out, case.get("expect", []))

cases = json.load(open("model_cases.json", encoding="utf-8"))
categories = list(dict.fromkeys(c["category"] for c in cases))
models = sys.argv[1:] or read_models()
rows = []
print(f"{'μοντέλο':<30}" + "".join(f"{c[:9]:>10}" for c in categories) + f"{'σύνολο':>9}{'χρόνος':>9}{'κόστος':>10}")
for model in models:
    ok = {c: 0 for c in categories}
    total = {c: 0 for c in categories}
    seconds, cost, errors = 0.0, 0.0, []
    for case in cases:
        out, s, c, err = ask(model, case["prompt"], tools=TOOLS if "tool" in case else None)
        total[case["category"]] += 1
        ok[case["category"]] += (not err) and correct(case, out)
        seconds, cost = seconds + s, cost + c
        if err:
            errors.append(f"{case['category']}: {err}")
    score = sum(ok.values()) / len(cases)
    print(f"{model:<30}" + "".join(f"{f'{ok[c]}/{total[c]}':>10}" for c in categories) + f"{score:>8.0%}{seconds / len(cases):>8.1f}s{cost:>10.5f}")
    for e in sorted(set(errors)):
        print(f"   ! {e}")
    rows.append({"model": model, "score": round(score, 3), "avg_seconds": round(seconds / len(cases), 2), "cost": round(cost, 6), **{c: ok[c] for c in categories}})
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print("\nΤα αποτελέσματα στο results.csv · γράφημα: python compare_chart.py")
