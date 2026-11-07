"""Διάλεξη 12: αναζήτηση με λέξεις ή με νόημα; Η ίδια ερώτηση στο FAQ με δύο τρόπους.

Χρήση:  python keyword_vs_meaning.py
        python keyword_vs_meaning.py "Η καφετιέρα βγάζει καπνούς"
"""
import re
import sys
from pythia_embed import embed, load_faq, faq_text, top_k

def words(text):
    return set(re.findall(r"\w+", text.lower()))

query = sys.argv[1] if len(sys.argv) > 1 else "Η καφετιέρα βγάζει καπνούς"
faq = load_faq()

print(f"Ερώτηση: «{query}»\n\n=== Με λέξεις (κοινές λέξεις) ===")
scored = [(len(words(query) & words(faq_text(item))), item) for item in faq]
scored.sort(key=lambda pair: pair[0], reverse=True)
for score, item in scored[:3]:
    print(f"  {score} λέξεις   {item['id']} {item['question']}")

print("\n=== Με νόημα (embeddings) ===")
faq_vectors = embed([faq_text(item) for item in faq])
query_vector = embed([query])[0]
for similarity, item in top_k(query_vector, faq, faq_vectors, 3):
    print(f"  {similarity:.2f}       {item['id']} {item['question']}")
