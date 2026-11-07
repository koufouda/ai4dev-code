"""Τρέχει όλα τα scripts του μαθήματος και γράφει τα αποτελέσματα σε ένα αρχείο.

Χρήση:  python selftest.py
Το αρχείο selftest_log.txt γράφεται στον φάκελο Week01 του Drive (αν υπάρχει),
ώστε να μπορεί να το διαβάσει ο Claude. Τα κλειδιά API δεν γράφονται ποτέ στο αρχείο.
"""
import os
import re
import subprocess
import sys
import time

DRIVE = r"G:\My Drive\AllData\Documents\01.Ιδιωτικά Κείμενα\AI for Developers\Week01"
if os.path.isdir(DRIVE):
    log_path = os.path.join(DRIVE, "selftest_log.txt")
else:
    log_path = "selftest_log.txt"

TESTS = [
    ("check", ["check.py"], "", 300),
    ("tokens", ["tokens.py"], "", 120),
    ("tokens λέξεις", ["tokens.py", "Θεσσαλονίκη", "νοημοσύνη", "intelligence"], "", 120),
    ("next_token", ["next_token.py", "Το πρωί πίνω έναν"], "", 120),
    ("chatbot", ["chatbot.py"], "Γεια, με λένε Μαρία και είμαι backend developer\nΠώς με λένε και τι δουλειά κάνω;\nτέλος\n", 180),
    ("step1", ["live/step1.py"], "", 120),
    ("step2", ["live/step2.py"], "", 120),
    ("step3", ["live/step3.py"], "", 120),
    ("ask cloud", ["ask.py", "Γεια σου"], "", 120),
    ("ask local", ["ask.py", "--local", "Γεια σου"], "", 300),
    ("pythia", ["pythia.py", "Να αλλάξω δουλειά;"], "", 180),
    ("temperature", ["temperature.py"], "", 600),
    ("stream cloud", ["stream.py"], "", 180),
    ("stream local", ["stream.py", "--local"], "", 600),
    ("arena", ["arena.py", "Εξήγησε τι είναι το API σε 2 προτάσεις."], "\n", 600),
]

def hide_keys(text):
    text = re.sub(r"sk-[A-Za-z0-9_\-]{6,}", "sk-***", text)
    text = re.sub(r"AIza[A-Za-z0-9_\-]{10,}", "AIza***", text)
    return text

env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"

report = []
report.append("Python: " + sys.version)

for name, args, keyboard, limit in TESTS:
    print("Τρέχει:", name, "...", flush=True)
    start = time.perf_counter()
    try:
        result = subprocess.run([sys.executable] + args, input=keyboard, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=limit, env=env)
        output = result.stdout + result.stderr
        status = "κωδικός εξόδου " + str(result.returncode)
    except subprocess.TimeoutExpired:
        output = ""
        status = "ΕΛΗΞΕ Ο ΧΡΟΝΟΣ (" + str(limit) + "s)"
    seconds = time.perf_counter() - start
    report.append("\n" + "=" * 70 + "\n" + name + " | python " + " ".join(args) + " | " + status + f" | {seconds:.1f}s\n" + "=" * 70)
    report.append(hide_keys(output)[-4000:])

with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("\nΈτοιμο. Το αποτέλεσμα είναι στο:", log_path)
