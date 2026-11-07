"""Διάλεξη 21: το eval των εργαλείων ως «πύλη» στο CI. Αποτυγχάνει (exit code 1) αν:
- κληθεί έστω και ένα απαγορευμένο εργαλείο, ή
- τα σωστά εργαλεία πέσουν κάτω από ένα όριο.
Θέλει κλειδί (κοστίζει λίγα σεντ): στο GitHub τρέχει μόνο όταν το ζητήσουμε.

Χρήση:  python ci_eval.py
        python ci_eval.py --min 0.9
"""
import sys
import json
import os
from pythia_tools import chat_with_tools
from pythia_rag import option

minimum = float(option(sys.argv, "--min", 0.8))
cases = json.load(open("tool_cases.json", encoding="utf-8"))
right, forbidden = 0, []
for case in cases:
    _, trace, _ = chat_with_tools(case["question"])
    called = {name for name, _, _ in trace}
    right += set(case["tools"]) <= called
    if set(case["forbidden"]) & called:
        forbidden.append(case["question"])
score = right / len(cases)
summary = f"Σωστά εργαλεία: {right}/{len(cases)} ({score:.0%}, όριο {minimum:.0%}) · Απαγορευμένα: {len(forbidden)}"
print(summary + "".join(f"\n  ✗ {q}" for q in forbidden))
if os.getenv("GITHUB_STEP_SUMMARY"):
    open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8").write("### Eval εργαλείων\n" + summary + "\n")
sys.exit(1 if forbidden or score < minimum else 0)
