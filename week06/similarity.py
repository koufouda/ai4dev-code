"""Διάλεξη 12: πόσο μοιάζουν κείμενα μεταξύ τους, σε αριθμούς.

Χρήση:  python similarity.py
"""
from pythia_embed import embed, cosine

sentences = [
    "Η μηχανή καφέ στάζει νερό.",
    "Η καφετιέρα έχει διαρροή από κάτω.",
    "The coffee machine is leaking water.",
    "i mixani kafe stazei nero",
    "Πότε θα έρθει η παραγγελία μου;",
    "Ο Παρθενώνας χτίστηκε τον 5ο αιώνα π.Χ.",
]
vectors = embed(sentences)

print("     " + "".join(f"{j + 1:>6}" for j in range(len(sentences))))
for i, a in enumerate(vectors):
    row = "".join(f"{cosine(a, b):>6.2f}" for b in vectors)
    print(f"{i + 1:>4} {row}   {sentences[i]}")
