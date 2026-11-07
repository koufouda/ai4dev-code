"""Διάλεξη 15: «δεν ξέρω». Ερωτήσεις που ΔΕΝ απαντώνται από τα έγγραφα, με και χωρίς κατώφλι.

Χρήση:  python idk_demo.py
        python idk_demo.py --threshold 7
"""
import json
import sys
from pythia_rag import load_index, search, answer, option
from pythia_safe import ask_safe

threshold = int(option(sys.argv, "--threshold", "5"))
questions = [q["question"] for q in json.load(open("unanswerable.json", encoding="utf-8"))]
index = load_index()
for q in questions:
    print(f"\n### {q}")
    text, _ = answer(q, search(index, q, "vector", 4))
    print(f"  Πριν (εβδ. 7):  {text.strip()[:110]}")
    r = ask_safe(index, q, threshold=threshold)
    print(f"  Μετά:           {r['answer'][:110]}" + (f"   [{r['refused']}]" if r["refused"] else ""))
