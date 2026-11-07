"""Διάλεξη 17: αξιολόγηση εργαλείων. Κάλεσε το μοντέλο τα σωστά εργαλεία; Απέφυγε τα απαγορευμένα; Είναι σωστή η απάντηση;

tool_cases.json: για κάθε ερώτηση, ποια εργαλεία ΠΡΕΠΕΙ να κληθούν (tools), ποια ΔΕΝ πρέπει (forbidden),
και τι πρέπει να περιέχει η απάντηση (expect, με «|» για εναλλακτικές).
ΠΡΟΣΟΧΗ: οι ακυρώσεις γράφονται στο actions.log (δεν αλλάζει το orders.json).

Χρήση:  python eval_tools.py
"""
import json
import time
from pythia_tools import chat_with_tools, contains_all

cases = json.load(open("tool_cases.json", encoding="utf-8"))
right_tools, no_forbidden, right_answer = 0, 0, 0
total_cost, total_calls = 0.0, 0
start = time.perf_counter()
for case in cases:
    answer, trace, cost = chat_with_tools(case["question"])
    called = {name for name, _, _ in trace}
    ok_tools = set(case["tools"]) <= called
    ok_forbidden = not (set(case["forbidden"]) & called)
    ok_answer = contains_all(answer, case["expect"])
    right_tools += ok_tools
    no_forbidden += ok_forbidden
    right_answer += ok_answer
    total_cost += cost
    total_calls += len(trace)
    marks = "".join("✓" if ok else "✗" for ok in (ok_tools, ok_forbidden, ok_answer))
    print(f"{marks}  {case['question'][:45]:<46} κάλεσε: {', '.join(sorted(called)) or '-'}")
n = len(cases)
print(f"\nΣωστά εργαλεία:        {right_tools}/{n}\nΧωρίς απαγορευμένα:    {no_forbidden}/{n}\nΣωστή απάντηση:        {right_answer}/{n}")
print(f"{total_calls} κλήσεις εργαλείων | ${total_cost:.4f} | {time.perf_counter() - start:.0f}s")
