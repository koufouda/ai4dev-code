"""Διάλεξη 9: ένα email γίνεται ticket που μπορεί να διαβάσει ο κώδικας.

Χρήση:  python ticket.py samples/01_kathysterisi.txt
        python ticket.py --local samples/03_kapnos.txt
"""
import os
import sys
from pythia_ticket import extract_ticket

args = sys.argv[1:]
model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
if "--local" in args:
    args.remove("--local")
    model = os.getenv("MODEL_LOCAL", "ollama_chat/gemma3:4b")
path = "samples/01_kathysterisi.txt"
if len(args) > 0:
    path = args[0]

text = open(path, encoding="utf-8").read()
ticket, seconds, cost = extract_ticket(text, model=model)

print(ticket.model_dump_json(indent=2))
print(f"\n[{model}] {seconds:.1f}s | ${cost:.6f}")

if ticket.priority == "υψηλή":
    print("→ ΕΠΕΙΓΟΝ: SMS στον υπεύθυνο βάρδιας")
elif ticket.category == "επιστροφή":
    print("→ Δημιουργία κουπονιού επιστροφής για την αποθήκη")
else:
    print("→ Στη γενική ουρά της εξυπηρέτησης")
