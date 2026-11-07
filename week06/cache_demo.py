"""Διάλεξη 11: prompt caching. Ο ίδιος μεγάλος κατάλογος σε τρεις ερωτήσεις.

Η πρώτη κλήση γράφει τον κατάλογο στην cache του παρόχου. Οι επόμενες τον διαβάζουν από εκεί:
πιο φθηνά και πιο γρήγορα. Η cache ζει περίπου 5 λεπτά.

Χρήση:  python cache_demo.py
        python cache_demo.py --no-cache     (το ίδιο χωρίς cache, για σύγκριση)
"""
import sys
from pythia_memory import MODEL, ask

catalog = open("katalogos.txt", encoding="utf-8").read()
text = "Είσαι η Πυθία του e-shop «Μπρίκι». Απαντάς σε μία πρόταση, μόνο από τον κατάλογο.\n\n<katalogos>\n" + catalog + "\n</katalogos>"
block = {"type": "text", "text": text}
if "--no-cache" not in sys.argv:
    block["cache_control"] = {"type": "ephemeral"}
system = {"role": "system", "content": [block]}
questions = ["Πόσο κοστίζει η ΜΠ-001;", "Έχετε μύλο καφέ κάτω από 50 €;", "Ποια είναι η πολιτική επιστροφών;"]

print(f"{'#':<3}{'είσοδος':>9}{'γράφτηκαν':>11}{'διαβάστηκαν':>13}{'κόστος $':>11}{'χρόνος':>8}  απάντηση")
for i, question in enumerate(questions, start=1):
    answer, n, seconds = ask([system, {"role": "user", "content": question}], MODEL, "cache_demo")
    print(f"{i:<3}{n['input']:>9}{n['cache_write']:>11}{n['cache_read']:>13}{n['cost']:>11.5f}{seconds:>7.1f}s  {answer[:60]}")
