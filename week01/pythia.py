"""Διάλεξη 2: το ίδιο μοντέλο με τρεις «προσωπικότητες». Αλλάζει μόνο το system prompt.

Χρήση:  python pythia.py        (Πυθία, η προεπιλογή)
        python pythia.py 1      (Βοηθός)
        python pythia.py 3      (Senior dev)
Γράψτε «τέλος» για έξοδο.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

PERSONAS = {
    "Βοηθός": "Είσαι χρήσιμος βοηθός. Απαντάς σύντομα και καθαρά.",
    "Πυθία": ("Είσαι η Πυθία των Δελφών. Απαντάς σε δύο γραμμές, με αρχαιοπρεπές ύφος "
              "και πάντα διφορούμενα, ώστε η απάντηση να βγαίνει σωστή ό,τι κι αν συμβεί."),
    "Senior dev": "Είσαι κουρασμένος senior developer. Σε κάθε ερώτηση απαντάς «εξαρτάται» και εξηγείς από τι.",
}

names = list(PERSONAS)
try:
    choice = int(sys.argv[1]) if len(sys.argv) > 1 else 2
except ValueError:
    choice = 0
if choice not in (1, 2, 3):
    print("Δώστε 1, 2 ή 3:", ", ".join(f"{i}={n}" for i, n in enumerate(names, 1)))
    sys.exit(1)
persona = names[choice - 1]

model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
history = [{"role": "system", "content": PERSONAS[persona] + " Απαντάς πάντα στα Ελληνικά."}]
print(f"Persona: {persona}  (γράψτε «τέλος» για έξοδο)")

while True:
    question = input("Εσύ: ")
    if question.lower().strip() in ("τέλος", "τελος", "exit", "quit"):
        break

    history.append({"role": "user", "content": question})
    response = completion(model=model, messages=history, num_retries=3)
    ai_answer = response.choices[0].message.content
    print(f"{persona}:", ai_answer)
    history.append({"role": "assistant", "content": ai_answer})
