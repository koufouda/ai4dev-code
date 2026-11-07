"""Διάλεξη 16, τελικό demo: όλα μαζί. Guardrails, cache, router, κώδικας ή RAG ή LLM με fallback.

Για κάθε ερώτηση δείχνει τη διαδρομή: κάθε βήμα με χρόνο και κόστος (trace).

Χρήση:  python pipeline_demo.py                 (ρωτά συνέχεια, «τέλος» για έξοδο)
        python pipeline_demo.py "Πού είναι η παραγγελία 48213;"
"""
import sys
from pythia_rag import load_index
from pythia_arch import pipeline

index = load_index()

def run(question):
    answer, trace = pipeline(index, question)
    for name, ms, cost, note in trace:
        print(f"   {name:<20}{ms:>6} ms  ${cost:.5f}  {note}")
    print(f"   {'ΣΥΝΟΛΟ':<20}{sum(s[1] for s in trace):>6} ms  ${sum(s[2] for s in trace):.5f}")
    print(f"Πυθία: {answer}\n")

if len(sys.argv) > 1:
    run(sys.argv[1])
else:
    while True:
        question = input("Ερώτηση: ")
        if question == "τέλος":
            break
        run(question)
