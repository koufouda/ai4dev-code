"""Διάλεξη 13: πριν και μετά το καθάρισμα μιας σελίδας PDF.

Χρήση:  python clean_demo.py
        python clean_demo.py docs/Eggyisi_kai_Service.pdf 2
"""
import sys
from pythia_rag import read_pdf, clean_pages

path = sys.argv[1] if len(sys.argv) > 1 else "docs/MP-001_Egxeiridio.pdf"
number = int(sys.argv[2]) if len(sys.argv) > 2 else 1
raw = read_pdf(path)
clean = dict(clean_pages(raw))
before = raw[number - 1][1]

print("===== ΠΡΙΝ =====")
print(before[:500])
print("\n===== ΜΕΤΑ =====")
print(clean.get(number, "")[:500])
print(f"\nΚομμένες λέξεις που ενώθηκαν: {before.count(chr(45) + chr(10))}")
