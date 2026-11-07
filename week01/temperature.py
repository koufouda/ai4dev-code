"""Διάλεξη 2: η ίδια ερώτηση 4 φορές με temperature 0 και 4 φορές με temperature 1.

Χρήση:  python temperature.py "Δώσε ένα όνομα για ένα καφέ στην Πλάκα."

Τρέχει στο τοπικό μοντέλο (MODEL_LOCAL), γιατί τα νεότερα Claude δέχονται μόνο temperature=1.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

model = os.getenv("MODEL_LOCAL", "ollama_chat/gemma3:4b")
prompt = " ".join(sys.argv[1:])
if prompt == "":
    prompt = "Δώσε ένα όνομα για ένα καφέ στην Πλάκα. Μόνο το όνομα."
print(f"[{model}]")

for t in [0.0, 1.0]:
    print(f"\ntemperature = {t}")
    for i in range(4):
        message = {"role": "user", "content": prompt}
        resp = completion(model=model, messages=[message], temperature=t)
        answer = resp.choices[0].message.content.strip()
        print(f"  {i + 1}. {answer}")
