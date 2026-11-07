"""Διάλεξη 17: η Πυθία με όλα τα εργαλεία. Για κάθε ερώτηση: ποια εργαλεία κάλεσε, με ποια ορίσματα, και η απάντηση.

Χρήση:  python tools_demo.py
        python tools_demo.py "Ακύρωσε την παραγγελία 48213 και στείλε μου μια ΜΠ-002"
"""
import sys
from pythia_tools import chat_with_tools, print_trace

questions = sys.argv[1:] or [
    "Πόσο κάνουν 3 συσκευασίες ΜΠ-004 με έκπτωση 10%;",
    "Έχετε μύλο καφέ κάτω από 60 €;",
    "Η παραγγελία μου 51007: η μηχανή γράφει E05. Τι κάνω;",
    "Ακύρωσε την παραγγελία 48213 και στείλε μου μια ΜΠ-002",
    "Ευχαριστώ πολύ!",
]
for q in questions:
    answer, trace, cost = chat_with_tools(q)
    print(f"### {q}")
    print_trace(trace)
    print(f"Πυθία: {answer}\n   [{len(trace)} εργαλεία | ${cost:.5f}]\n")
