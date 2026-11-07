"""Διάλεξη 17: η Πυθία ΧΩΡΙΣ εργαλεία. Τρεις ερωτήσεις που θέλουν δεδομένα ή πράξεις.

Χρήση:  python no_tools.py
"""
from pythia_rag import MODEL, completion

questions = [
    "Πόσο κοστίζει η ΜΠ-001;",
    "Πού είναι η παραγγελία 48213;",
    "Πόσο κάνουν 3 συσκευασίες ΜΠ-004 με έκπτωση 10%;",
]
for q in questions:
    resp = completion(model=MODEL, messages=[{"role": "system", "content": "Είσαι η Πυθία, βοηθός του e-shop «Μπρίκι». Απάντα σε 1-2 προτάσεις."}, {"role": "user", "content": q}], num_retries=3)
    print(f"### {q}\n{resp.choices[0].message.content}\n")
print("Σωστά: 349.00 € · «σε μεταφορά», αύριο 10:00-14:00 · 3 × 10.36 × 0.9 = 27.97 €")
