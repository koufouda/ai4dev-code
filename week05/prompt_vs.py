"""Διάλεξη 9: το ίδιο email, δύο prompts. Ποιο δίνει πιο χρήσιμη απάντηση;

Χρήση:  python prompt_vs.py
        python prompt_vs.py samples/06_dipli_xreosi.txt
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
path = "samples/01_kathysterisi.txt"
if len(sys.argv) > 1:
    path = sys.argv[1]
email = open(path, encoding="utf-8").read()

bad = "Τι λέει αυτό το email;\n\n" + email
good = (
    "Είσαι υπάλληλος εξυπηρέτησης πελατών σε e-shop με μηχανές καφέ.\n"
    "Διάβασε το email ανάμεσα στις ετικέτες <email>.\n"
    "Απάντησε σε τρεις γραμμές:\n"
    "1. Τι ζητά ο πελάτης (μία πρόταση)\n"
    "2. Πόσο επείγει: υψηλή, μεσαία ή χαμηλή, και γιατί\n"
    "3. Ποια είναι η επόμενη ενέργεια για εμάς\n"
    "Μην προσθέσεις τίποτα άλλο.\n\n"
    "<email>\n" + email + "\n</email>"
)

for title, prompt in [("ΚΑΚΟ PROMPT", bad), ("ΚΑΛΟ PROMPT", good)]:
    message = {"role": "user", "content": prompt}
    resp = completion(model=model, messages=[message], num_retries=3)
    print(f"\n===== {title} =====")
    print(resp.choices[0].message.content)
    print(f"[{resp.usage.completion_tokens} tokens απάντησης]")
