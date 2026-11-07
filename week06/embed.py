"""Διάλεξη 12: ένα κείμενο γίνεται διάνυσμα (λίστα αριθμών).

Χρήση:  python embed.py
        python embed.py "Η μηχανή στάζει νερό"
"""
import sys
import time
from pythia_embed import EMBED_MODEL, embed

text = sys.argv[1] if len(sys.argv) > 1 else "Η μηχανή καφέ στάζει νερό"
start = time.perf_counter()
vector = embed([text])[0]
seconds = time.perf_counter() - start

print(f"Κείμενο: «{text}»   [{EMBED_MODEL}, {seconds:.2f}s]")
print(f"Διαστάσεις: {len(vector)}")
print("Οι 8 πρώτοι αριθμοί:", [round(x, 4) for x in vector[:8]])
print(f"Από {min(vector):.4f} έως {max(vector):.4f}")
