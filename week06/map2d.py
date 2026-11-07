"""Διάλεξη 12: ο «χάρτης» του νοήματος. Τα διανύσματα του FAQ σε δύο διαστάσεις, σε εικόνα.

Από εκατοντάδες διαστάσεις κρατάμε τις 2 που εξηγούν τις περισσότερες διαφορές (PCA).
Ερωτήσεις με παρόμοιο νόημα πέφτουν κοντά.

Χρήση:  python map2d.py
        python map2d.py "Η καφετιέρα βγάζει καπνούς"     (δείχνει και την ερώτηση στον χάρτη)
Βγάζει το αρχείο map.png.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from pythia_embed import EMBED_MODEL, embed, load_faq, faq_text

faq = load_faq()
texts = [faq_text(item) for item in faq]
query = sys.argv[1] if len(sys.argv) > 1 else None
if query:
    texts.append(query)
X = np.array(embed(texts))
X = X - X.mean(axis=0)
_, _, directions = np.linalg.svd(X, full_matrices=False)
points = X @ directions[:2].T

categories = sorted({item["category"] for item in faq})
plt.figure(figsize=(11, 8))
for category in categories:
    rows = [i for i, item in enumerate(faq) if item["category"] == category]
    plt.scatter(points[rows, 0], points[rows, 1], s=80, label=category)
for i, item in enumerate(faq):
    plt.annotate(item["id"] + " " + item["question"][:28], points[i], fontsize=8)
if query:
    plt.scatter(points[-1, 0], points[-1, 1], s=300, marker="*", color="black", label="ερώτηση")
    plt.annotate(query, points[-1], fontsize=11, fontweight="bold")
plt.title(f"Το FAQ του «Μπρίκι» σε 2 διαστάσεις ({EMBED_MODEL})")
plt.legend()
plt.savefig("map.png", dpi=120, bbox_inches="tight")
print("Έγινε: map.png (ανοίξτε το από το VS Code ή με διπλό κλικ)")
