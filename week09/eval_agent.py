"""Διάλεξη 18: αξιολόγηση του agent. Σωστές απαντήσεις, βήματα, κόστος, χρόνος, γιατί σταμάτησε.

agent_cases.json: για κάθε εργασία, τι πρέπει να περιέχει η απάντηση (expect, με «|» για εναλλακτικές).
ΠΡΟΣΟΧΗ: οι ακυρώσεις γράφονται στο actions.log.

Χρήση:  python eval_agent.py
        python eval_agent.py --workflow         (οι ίδιες εργασίες με σταθερά βήματα)
        python eval_agent.py --max-steps 4
"""
import sys
import json
from pythia_agent import agent, fixed_workflow
from pythia_tools import contains_all
from pythia_rag import option

max_steps = int(option(sys.argv, "--max-steps", 8))
cases = json.load(open("agent_cases.json", encoding="utf-8"))
results = []
for case in cases:
    r = fixed_workflow(case["task"]) if "--workflow" in sys.argv else agent(case["task"], max_steps=max_steps, verbose=False)
    r["ok"] = contains_all(r["answer"], case["expect"])
    results.append(r)
    print(f"{'✓' if r['ok'] else '✗'}  {case['task'][:55]:<56} {len(r['steps']):>2} ενέργειες  ${r['cost']:.5f}  {r['seconds']:5.1f}s  {r['stopped']}")
n = len(results)
print(f"\nΣωστά: {sum(r['ok'] for r in results)}/{n} | μέσος όρος: {sum(len(r['steps']) for r in results) / n:.1f} ενέργειες, "
      f"${sum(r['cost'] for r in results) / n:.5f}, {sum(r['seconds'] for r in results) / n:.1f}s ανά εργασία")
