"""Διάλεξη 9: ζητάμε JSON «με το στόμα». Πόσο εύθραυστο είναι;

Χρήση:  python json_please.py
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
email = open("samples/06_dipli_xreosi.txt", encoding="utf-8").read()
prompt = "Βγάλε από το email σε JSON την κατηγορία, την προτεραιότητα και τον αριθμό παραγγελίας.\n\n" + email

for i in range(1, 4):
    resp = completion(model=model, messages=[{"role": "user", "content": prompt}], num_retries=3)
    raw = resp.choices[0].message.content
    print(f"\n===== Προσπάθεια {i} =====")
    print(raw)
    try:
        data = json.loads(raw)
        print("→ OK, κλειδιά:", list(data.keys()))
    except json.JSONDecodeError as e:
        print("→ ΑΠΕΤΥΧΕ το json.loads:", e)
