"""Διάλεξη 17: workflow. Ο ΚΩΔΙΚΑΣ ορίζει τα βήματα· το μοντέλο κάνει μόνο ό,τι του αναθέτει κάθε βήμα.

Email παραπόνου → 1. εξαγωγή στοιχείων (LLM, σχήμα) → 2. παραγγελία (κώδικας) → 3. έγγραφα (αναζήτηση)
→ 4. προσχέδιο απάντησης (LLM) → 5. έλεγχος (κώδικας): αποστολή ή άνθρωπος.

Χρήση:  python workflow.py          (τα 3 email του emails.json)
        python workflow.py 2        (μόνο το 2ο)
"""
import sys
import json
import time
from typing import Literal
from pydantic import BaseModel, Field
from pythia_rag import MODEL, completion, safe_cost
from pythia_tools import get_order, search_docs
from pythia_safe import output_guard

class Complaint(BaseModel):
    order_id: str | None = Field(description="Πενταψήφιος αριθμός παραγγελίας, ή null αν δεν αναφέρεται")
    problem: str = Field(description="Το πρόβλημα σε λίγες λέξεις, για αναζήτηση στα έγγραφα")
    wants: Literal["επιστροφή", "αντικατάσταση", "πληροφορία", "ακύρωση", "άλλο"]
    angry: bool = Field(description="true αν ο πελάτης είναι θυμωμένος")

def handle(email):
    cost = 0.0
    t = time.perf_counter()
    resp = completion(model=MODEL, messages=[{"role": "user", "content": "Βγάλε τα στοιχεία από το email πελάτη:\n<email>" + email["text"] + "</email>"}], response_format=Complaint, num_retries=3)
    c = Complaint.model_validate_json(resp.choices[0].message.content)
    cost += safe_cost(resp, MODEL)
    print(f"{'1. εξαγωγή (LLM)':<24}{(time.perf_counter() - t) * 1000:5.0f} ms  {c.model_dump()}")
    t = time.perf_counter()
    order = get_order(c.order_id) if c.order_id else "Ο πελάτης δεν έδωσε αριθμό παραγγελίας."
    print(f"{'2. παραγγελία (κώδικας)':<24}{(time.perf_counter() - t) * 1000:5.0f} ms  {order[:80]}")
    t = time.perf_counter()
    docs = search_docs(c.problem)
    print(f"{'3. έγγραφα (αναζήτηση)':<24}{(time.perf_counter() - t) * 1000:5.0f} ms  {' '.join(docs.split())[:80]}")
    t = time.perf_counter()
    user = f"<email>{email['text']}</email>\n<order>{order}</order>\n<documents>{docs}</documents>\nΓράψε απάντηση 3-4 προτάσεων στον πελάτη, μόνο από τα παραπάνω."
    resp = completion(model=MODEL, messages=[{"role": "system", "content": "Είσαι η εξυπηρέτηση του e-shop «Μπρίκι». Ευγενικά, σύντομα, στα ελληνικά."}, {"role": "user", "content": user}], num_retries=3)
    draft = resp.choices[0].message.content
    cost += safe_cost(resp, MODEL)
    print(f"{'4. προσχέδιο (LLM)':<24}{(time.perf_counter() - t) * 1000:5.0f} ms")
    problems = output_guard(draft) + (["θυμωμένος πελάτης"] if c.angry else []) + (["ζητά επιστροφή χρημάτων"] if c.wants == "επιστροφή" else [])
    decision = "ΣΤΟΝ ΑΝΘΡΩΠΟ: " + ", ".join(problems) if problems else "αποστολή"
    print(f"{'5. έλεγχος (κώδικας)':<24}   → {decision}\n\n{draft}\n\n   [2 κλήσεις LLM | ${cost:.5f}]")

emails = json.load(open("emails.json", encoding="utf-8"))
if len(sys.argv) > 1:
    emails = [emails[int(sys.argv[1]) - 1]]
for e in emails:
    print(f"\n{'=' * 20} {e['from']}: «{e['text'][:60]}…» {'=' * 20}")
    handle(e)
