"""Διάλεξη 18: ο agent λύνει εργασίες πολλών βημάτων. Κάθε βήμα: σκέψη, ενέργεια, παρατήρηση.

Χρήση:  python agent_demo.py                    (ρωτά συνέχεια, «τέλος» για έξοδο)
        python agent_demo.py "Η παραγγελία 41188 έχει μια ΜΠ-001 που γράφει E05. Καλύπτεται από την εγγύηση;"
"""
import sys
from pythia_agent import agent

def run(task):
    print(f"\n### {task}")
    r = agent(task)
    print(f"\n   [{len(r['steps'])} ενέργειες | ${r['cost']:.5f} | {r['seconds']:.1f}s | σταμάτησε: {r['stopped']}]")

if len(sys.argv) > 1:
    run(sys.argv[1])
else:
    while True:
        task = input("\nΕργασία: ")
        if task == "τέλος":
            break
        run(task)
