"""Διάλεξη 12: αναζήτηση με νόημα στη vector database. Τρέξτε πρώτα το build_index.py.

Χρήση:  python search.py "Η καφετιέρα βγάζει καπνούς"
        python search.py "πότε φτάνει το δέμα" --k 5
        python search.py "ζεστός καφές" --category συσκευές
        python search.py                         (ρωτά συνέχεια, «τέλος» για έξοδο)
"""
import sys
import chromadb
from pythia_embed import embed, option

k = int(option(sys.argv, "--k", "3"))
category = option(sys.argv, "--category", None)
collection = chromadb.PersistentClient(path="db").get_collection("faq")

def search(query):
    where = {"category": category} if category else None
    result = collection.query(query_embeddings=embed([query]), n_results=k, where=where)
    for id_, distance, document in zip(result["ids"][0], result["distances"][0], result["documents"][0]):
        print(f"  {1 - distance:.2f}  {id_}  {document.splitlines()[0]}")

if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
    search(sys.argv[1])
else:
    while True:
        query = input("\nΕρώτηση: ")
        if query == "τέλος":
            break
        search(query)
