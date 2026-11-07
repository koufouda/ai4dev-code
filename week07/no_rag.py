"""Διάλεξη 13, άνοιγμα: η Πυθία χωρίς έγγραφα. Τι απαντά για πράγματα που ξέρει μόνο το e-shop;

Χρήση:  python no_rag.py
        python no_rag.py "Τι σημαίνει το σφάλμα E05 στη ΜΠ-001;"
"""
import sys
from pythia_rag import MODEL, completion

question = sys.argv[1] if len(sys.argv) > 1 else "Πόσους μήνες εγγύηση έχει η μηχανή espresso Αστέρι ΜΠ-001 και τι δεν καλύπτει;"
system = "Είσαι η Πυθία, βοηθός του e-shop «Μπρίκι». Απαντάς σύντομα, στα ελληνικά."
resp = completion(model=MODEL, messages=[{"role": "system", "content": system}, {"role": "user", "content": question}], num_retries=3)
print("Ερώτηση:", question)
print("\nΠυθία (χωρίς έγγραφα):", resp.choices[0].message.content)
