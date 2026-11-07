"""Διάλεξη 9, τελικό demo: όλα τα email του φακέλου samples γίνονται ουρά εργασιών.

Χρήση:  python inbox.py
        python inbox.py --local
"""
import glob
import os
import sys
import time
from pythia_ticket import extract_ticket

model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
if "--local" in sys.argv:
    model = os.getenv("MODEL_LOCAL", "ollama_chat/gemma3:4b")

paths = sorted(glob.glob("samples/*.txt"))
rows = []
total_cost = 0.0
start = time.perf_counter()

for path in paths:
    text = open(path, encoding="utf-8").read()
    ticket, seconds, cost = extract_ticket(text, model=model)
    total_cost += cost
    rows.append((os.path.basename(path), ticket))
    print(".", end="", flush=True)

order = {"υψηλή": 0, "μεσαία": 1, "χαμηλή": 2}
rows.sort(key=lambda row: order[row[1].priority])

print(f"\n\n{'Προτερ.':<8} {'Κατηγορία':<17} {'Παραγγ.':<8} Περίληψη")
for name, t in rows:
    order_number = t.order_number or "-"
    print(f"{t.priority:<8} {t.category:<17} {order_number:<8} {t.summary[:60]}")

print(f"\n{len(rows)} email σε {time.perf_counter() - start:.1f}s | ${total_cost:.4f} | [{model}]")
