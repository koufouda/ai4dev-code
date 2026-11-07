"""Διάλεξη 15: ένα έγγραφο με κρυφή εντολή μπαίνει στη βάση. Τι κάνει η Πυθία χωρίς και με άμυνες;

Το docs_attack/Fthinoporini_Prosfora.pdf έχει λευκό κείμενο (αόρατο στο μάτι) με εντολές προς τον βοηθό.
Η βάση φτιάχνεται στη μνήμη, για να μη «μολυνθεί» η κανονική βάση db/.

Χρήση:  python attack_demo.py
        python attack_demo.py "Έχετε κάποια προσφορά αυτή την περίοδο;"
"""
import sys
from pythia_rag import MODEL, completion, load_all, load_chunks, build_index, search
from pythia_safe import quarantine, ask_safe, output_guard

question = sys.argv[1] if len(sys.argv) > 1 else "Πώς παίρνω πίσω τα χρήματά μου αν επιστρέψω μια μηχανή;"
chunks = load_all() + load_chunks("docs_attack/Fthinoporini_Prosfora.pdf")
print(f"Ερώτηση: {question}\n")

print("=" * 20, "ΧΩΡΙΣ ΑΜΥΝΕΣ", "=" * 20)
index = build_index(chunks)
results = search(index, question, "hybrid", 4)
naive = "Απάντησε στην ερώτηση του πελάτη με βάση τα παρακάτω κείμενα.\n\n" + "\n\n".join(c["text"] for _, c in results) + "\n\nΕρώτηση: " + question
resp = completion(model=MODEL, messages=[{"role": "user", "content": naive}], num_retries=3)
text = resp.choices[0].message.content
print("Πυθία:", text)
print("Ο έλεγχος εξόδου θα έβρισκε:", output_guard(text) or "τίποτα")

print("\n" + "=" * 20, "ΜΕ ΑΜΥΝΕΣ", "=" * 20)
clean, suspicious = quarantine(chunks)
print(f"Καραντίνα: {len(suspicious)} κομμάτια {[c['id'] for c in suspicious]}")
index = build_index(clean)
r = ask_safe(index, question)
print("Πυθία:", r["answer"])
for c in r["citations"]:
    print(f"  {'✓' if c['ok'] else '✗'} {c['source']}: «{c['quote']}»")
if r["refused"]:
    print("Άρνηση:", r["refused"])
