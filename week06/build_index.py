"""Διάλεξη 12: βάζουμε το FAQ σε vector database (Chroma), μία φορά.

Τα διανύσματα αποθηκεύονται στον φάκελο db/. Το search.py τα διαβάζει από εκεί,
χωρίς να ξαναϋπολογίζει τα embeddings του FAQ.

Χρήση:  python build_index.py
"""
import time
import chromadb
from pythia_embed import EMBED_MODEL, embed, load_faq, faq_text

faq = load_faq()
start = time.perf_counter()
texts = [faq_text(item) for item in faq]
vectors = embed(texts)

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("faq", metadata={"hnsw:space": "cosine"})
collection.upsert(
    ids=[item["id"] for item in faq],
    embeddings=vectors,
    documents=texts,
    metadatas=[{"category": item["category"], "model": EMBED_MODEL} for item in faq],
)
print(f"Στη βάση: {collection.count()} στοιχεία | {len(vectors[0])} διαστάσεις | {time.perf_counter() - start:.1f}s | {EMBED_MODEL}")
