"""Διάλεξη 13: πώς κόβουμε ένα έγγραφο σε κομμάτια (chunks).

Χρήση:  python chunk_demo.py                    (κομμάτια με προτάσεις, 800 χαρακτήρες, overlap 150)
        python chunk_demo.py --size 400
        python chunk_demo.py --naive            (κόψιμο κάθε 800 χαρακτήρες, όπου κι αν πέσει)
        python chunk_demo.py --file docs/Oroi_Polisis.docx
"""
import sys
from pythia_rag import read_pdf, clean_pages, chunk_text, chunk_chars, load_chunks, option

path = option(sys.argv, "--file", "docs/MP-001_Egxeiridio.pdf")
size = int(option(sys.argv, "--size", "800"))
overlap = int(option(sys.argv, "--overlap", "150"))

if "--naive" in sys.argv:
    text = clean_pages(read_pdf(path))[0][1]
    chunks = chunk_chars(text, size)
    print(f"Αφελές κόψιμο κάθε {size} χαρακτήρες: {len(chunks)} κομμάτια στη σελίδα 1\n")
    for i, c in enumerate(chunks, 1):
        print(f"#{i}  «{c[:40]}» … «{c[-40:]}»")
else:
    chunks = load_chunks(path, size, overlap)
    print(f"{path}: {len(chunks)} κομμάτια | size {size} | overlap {overlap} | μέσο μήκος {sum(len(c['text']) for c in chunks) // len(chunks)} χαρακτήρες\n")
    for c in chunks[:3]:
        print(f"[{c['id']}]  «{c['text'][:60]}» … «{c['text'][-50:]}»\n")
