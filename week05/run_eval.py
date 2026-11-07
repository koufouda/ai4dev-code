"""Διάλεξη 10: τρέχει το σύνολο δοκιμών και δίνει σκορ.

Χρήση:  python run_eval.py                      (prompt v2, βασικό μοντέλο)
        python run_eval.py --prompt v1          (η παλιά εκδοχή των οδηγιών)
        python run_eval.py --model ollama_chat/gemma3:4b
        python run_eval.py --repeat 3           (κάθε δοκιμή 3 φορές)
"""
import json
import os
import sys
from pythia_ticket import extract_ticket

def option(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default

prompt = option("--prompt", "v2")
model = option("--model", os.getenv("MODEL", "anthropic/claude-haiku-5-5"))
repeat = int(option("--repeat", "1"))
cases = json.load(open("eval_cases.json", encoding="utf-8"))
fields = ["category", "priority", "order_number"]

passed = 0
total = 0
total_seconds = 0.0
total_cost = 0.0

print(f"prompt {prompt} | {model} | {len(cases)} δοκιμές x {repeat}\n")
for case in cases:
    text = open(case["file"], encoding="utf-8").read()
    for _ in range(repeat):
        ticket, seconds, cost = extract_ticket(text, model=model, prompt=prompt)
        total_seconds += seconds
        total_cost += cost
        marks = []
        for field in fields:
            expected = case[field]
            actual = getattr(ticket, field)
            total += 1
            if actual == expected:
                passed += 1
                marks.append("✓")
            else:
                marks.append(f"✗({actual})")
        print(f"{os.path.basename(case['file']):<24} " + "  ".join(marks))

score = passed / total * 100
print(f"\nΣΚΟΡ: {passed}/{total} = {score:.0f}% | {total_seconds:.1f}s | ${total_cost:.4f}")
