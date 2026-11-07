"""Διάλεξη 22: GDPR στην πράξη, πάνω στα logs της Πυθίας.
- Δικαίωμα πρόσβασης: όλα όσα έχουμε για έναν χρήστη.
- Δικαίωμα διαγραφής: σβήνουμε όλες τις γραμμές του.
- Περίοδος διατήρησης: σβήνουμε τα logs που είναι παλαιότερα από N ημέρες.

Χρήση:  python privacy.py --export user3
        python privacy.py --erase user3
        python privacy.py --retention 30
"""
import sys
import os
import json
import glob
import datetime
from pythia_rag import option
from app import pseudonym

export_user, erase_user, days = option(sys.argv, "--export", None), option(sys.argv, "--erase", None), option(sys.argv, "--retention", None)
paths = sorted(glob.glob("logs/*.jsonl"))

if export_user:
    p = pseudonym(export_user)
    rows = [json.loads(line) for path in paths for line in open(path, encoding="utf-8") if json.loads(line).get("user") == p]
    print(json.dumps(rows, ensure_ascii=False, indent=1))
    print(f"\n{len(rows)} εγγραφές για τον χρήστη {export_user} (ψευδώνυμο {p})")

if erase_user:
    p = pseudonym(erase_user)
    ids = {json.loads(line)["request_id"] for path in paths for line in open(path, encoding="utf-8") if json.loads(line).get("user") == p}
    removed = 0
    for path in paths:
        lines = open(path, encoding="utf-8").readlines()
        keep = [line for line in lines if json.loads(line).get("user") != p and json.loads(line)["request_id"] not in ids]
        removed += len(lines) - len(keep)
        open(path, "w", encoding="utf-8").writelines(keep)
    print(f"Σβήστηκαν {removed} εγγραφές του χρήστη {erase_user} (ερωτήσεις και feedback).")

if days:
    limit = datetime.date.today() - datetime.timedelta(days=int(days))
    for path in paths:
        day = datetime.date.fromisoformat(os.path.basename(path)[:10])
        if day < limit:
            os.remove(path)
            print("Σβήστηκε:", path)
    print(f"Κρατάμε logs μόνο από {limit} και μετά.")
