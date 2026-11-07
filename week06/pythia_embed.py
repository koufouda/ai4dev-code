"""Εβδομάδα 6, διάλεξη 12: κοινές συναρτήσεις για embeddings.

Το χρησιμοποιούν τα embed.py, similarity.py, keyword_vs_meaning.py, build_index.py, search.py,
eval_search.py και map2d.py.
"""
import json
import math
import os
from dotenv import load_dotenv

load_dotenv()
from litellm import embedding

EMBED_MODEL = os.getenv("EMBED_MODEL", "ollama/embeddinggemma")

def embed(texts, model=EMBED_MODEL):
    resp = embedding(model=model, input=texts)
    return [item["embedding"] for item in resp.data]

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)

def load_faq():
    return json.load(open("faq.json", encoding="utf-8"))

def faq_text(item):
    return item["question"] + "\n" + item["answer"]

def top_k(query_vector, faq, faq_vectors, k=3):
    scored = [(cosine(query_vector, v), item) for v, item in zip(faq_vectors, faq)]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored[:k]

def option(argv, name, default):
    if name in argv:
        return argv[argv.index(name) + 1]
    return default
