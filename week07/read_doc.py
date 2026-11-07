"""Διάλεξη 13: τι «βλέπει» ο υπολογιστής όταν διαβάζει ένα PDF ή ένα Word. Χωρίς καθάρισμα.

Χρήση:  python read_doc.py docs/MP-001_Egxeiridio.pdf
        python read_doc.py docs/Oroi_Polisis.docx
"""
import sys
from pythia_rag import read_pdf, read_docx

path = sys.argv[1] if len(sys.argv) > 1 else "docs/MP-001_Egxeiridio.pdf"
if path.lower().endswith(".pdf"):
    pages = read_pdf(path)
    print(f"{path}: {len(pages)} σελίδες\n")
    print("===== Σελίδα 1, ωμό κείμενο (οι αλλαγές γραμμής φαίνονται ως \\n) =====")
    print(repr(pages[0][1][:700]))
else:
    sections = read_docx(path)
    print(f"{path}: {len(sections)} ενότητες\n")
    for heading, text in sections:
        print(f"[{heading}]  {len(text)} χαρακτήρες: {text[:80]}…")
