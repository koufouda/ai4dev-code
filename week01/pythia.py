"""Διάλεξη 2: το system prompt αλλάζει την «προσωπικότητα» του ίδιου μοντέλου.

Χρήση:  python pythia.py "Να αλλάξω δουλειά;"
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
question = " ".join(sys.argv[1:])
if question == "":
    question = "Θα περάσω το μάθημα;"

PERSONAS = {
    "Βοηθός": "Είσαι χρήσιμος βοηθός. Απαντάς σύντομα και καθαρά.",
    "Πυθία": "Είσαι η Πυθία των Δελφών. Απαντάς σε δύο γραμμές, με αρχαιοπρεπές ύφος και πάντα διφορούμενα, ώστε η απάντηση να βγαίνει σωστή ό,τι κι αν συμβεί.",
    "Senior dev": "Είσαι κουρασμένος senior developer. Σε κάθε ερώτηση απαντάς «εξαρτάται» και εξηγείς από τι.",
}

for name, system in PERSONAS.items():
    system_message = {"role": "system", "content": system}
    user_message = {"role": "user", "content": question}
    resp = completion(model=model, messages=[system_message, user_message], num_retries=3)
    print(f"--- {name} ---")
    print(resp.choices[0].message.content + "\n")
