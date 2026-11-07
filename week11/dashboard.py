"""Διάλεξη 22: τι γίνεται στην παραγωγή; Διαβάζει τα logs/*.jsonl και δείχνει όγκο, σφάλματα, χρόνο,
κόστος, εργαλεία, προσωπικά δεδομένα που κρύφτηκαν, feedback, και ειδοποιήσεις όταν κάτι ξεφεύγει.

Χρήση:  python dashboard.py
        python dashboard.py --budget 0.50       (όριο κόστους ανά ημέρα σε $)
"""
import sys
import json
import glob
from collections import Counter
from pythia_rag import option

BUDGET = float(option(sys.argv, "--budget", 1.0))
MAX_ERRORS = 0.05
MAX_P95 = 15000
MAX_BAD = 0.30

events = [json.loads(line) for path in sorted(glob.glob("logs/*.jsonl")) for line in open(path, encoding="utf-8")]
chats = [e for e in events if e["type"] == "chat"]
feedback = [e for e in events if e["type"] == "feedback"]
if not chats:
    sys.exit("Δεν υπάρχουν logs. Τρέξτε πρώτα: python traffic.py")
times = sorted(e["ms"] for e in chats)
p95 = times[int(0.95 * (len(times) - 1))]
errors = sum(1 for e in chats if e["error"])
blocked = sum(1 for e in chats if e["blocked"])
cost_per_day = Counter()
for e in chats:
    cost_per_day[e["time"][:10]] += e["cost"]
tools = Counter(t for e in chats for t in e["tools"])
pii = Counter(p for e in chats for p in e["pii_masked"])
bad = sum(1 for f in feedback if not f["good"]) / len(feedback) if feedback else 0

print(f"Αιτήματα: {len(chats)} από {len({e['user'] for e in chats})} χρήστες · εκδόσεις: {', '.join(sorted({e['version'] for e in chats}))}")
print(f"Σφάλματα: {errors} ({errors / len(chats):.0%}) · Μπλοκαρισμένες απαντήσεις: {blocked}")
print(f"Χρόνος: μέσος {sum(times) / len(times):.0f} ms · p95 {p95} ms")
print("Κόστος ανά ημέρα: " + ", ".join(f"{day} ${c:.4f}" for day, c in sorted(cost_per_day.items())) + f" · ανά αίτημα ${sum(cost_per_day.values()) / len(chats):.5f}")
print("Εργαλεία:", dict(tools.most_common()))
print("Προσωπικά δεδομένα που κρύφτηκαν:", dict(pii) or "κανένα")
print(f"Feedback: {len(feedback)} · 👎 {bad:.0%}")

alerts = []
alerts += [f"κόστος {day}: ${c:.2f} > όριο ${BUDGET:.2f}" for day, c in cost_per_day.items() if c > BUDGET]
alerts += [f"σφάλματα {errors / len(chats):.0%} > {MAX_ERRORS:.0%}"] if errors / len(chats) > MAX_ERRORS else []
alerts += [f"p95 {p95} ms > {MAX_P95} ms"] if p95 > MAX_P95 else []
alerts += [f"👎 {bad:.0%} > {MAX_BAD:.0%}"] if bad > MAX_BAD else []
print("\n⚠ ΕΙΔΟΠΟΙΗΣΕΙΣ:\n  " + "\n  ".join(alerts) if alerts else "\n✓ Όλα μέσα στα όρια.")
