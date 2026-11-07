"""Διάλεξη 18: agent ή workflow; Οι ίδιες εργασίες με σταθερά βήματα και με agent. Σωστό, βήματα, κόστος, χρόνος.

Χρήση:  python agent_vs_workflow.py
"""
from pythia_agent import agent, fixed_workflow
from pythia_tools import contains_all

tasks = [
    ("Πού είναι η παραγγελία 48213;", ["μεταφορα"]),
    ("Πόσο κάνουν 3 συσκευασίες ΜΠ-004 με έκπτωση 10%;", ["27.97|27,97"]),
    ("Η παραγγελία 41188 έχει μια ΜΠ-001 που γράφει E05. Καλύπτεται ακόμα από την εγγύηση;", ["δεν καλυπτ|εκτος εγγυησ|εληξε|εχει ληξει"]),
]
print(f"{'εργασία':<48}{'τρόπος':<10}{'σωστό':>6}{'ενέργειες':>11}{'κόστος':>10}{'χρόνος':>8}")
for task, expect in tasks:
    for name, r in [("workflow", fixed_workflow(task)), ("agent", agent(task, verbose=False))]:
        print(f"{task[:46]:<48}{name:<10}{'✓' if contains_all(r['answer'], expect) else '✗':>6}{len(r['steps']):>11}{r['cost']:>10.5f}{r['seconds']:>7.1f}s")
    print()
