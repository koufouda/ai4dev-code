"""Διάλεξη 11: πόσο μεγαλώνει το κόστος μιας συνομιλίας, γύρο-γύρο. ΔΕΝ καλεί μοντέλο.

Μετρά τα tokens που θα στέλναμε σε κάθε γύρο με τρεις στρατηγικές μνήμης:
  full    = όλο το ιστορικό
  window  = μόνο τα 6 τελευταία μηνύματα
  summary = σύνοψη των παλιών και τα 4 τελευταία

Χρήση:  python growth.py
        python growth.py --turns 50
"""
import sys
from pythia_memory import MODEL, SYSTEM, count, window, price, option

turns = int(option(sys.argv, "--turns", "30"))
question = {"role": "user", "content": "Ποια μηχανή espresso μου προτείνετε για ένα γραφείο με δέκα άτομα που πίνουν δύο καφέδες τη μέρα;"}
answer = {"role": "assistant", "content": "Για δέκα άτομα σας προτείνω τη ΜΠ-001, γιατί βγάζει δύο καφέδες ταυτόχρονα και έχει δοχείο νερού 2 λίτρων. Κοστίζει 349 € και είναι διαθέσιμη. Θέλετε να δούμε και έναν μύλο που ταιριάζει;"}
summary = {"role": "system", "content": SYSTEM["content"] + "\n\nΣύνοψη: Ο πελάτης Γιώργος ψάχνει μηχανή espresso για γραφείο 10 ατόμων. Του προτείναμε τη ΜΠ-001 (349 €). Ενδιαφέρεται και για μύλο. Δεν έχει αποφασίσει."}
cost_in, _, estimated = price(MODEL)

history = [SYSTEM]
totals = {"full": 0, "window": 0, "summary": 0}

print(f"{'Γύρος':>5} {'full':>8} {'window':>8} {'summary':>8}   (tokens εισόδου ανά γύρο)")
for turn in range(1, turns + 1):
    history.append(question)
    full = count(history)
    win = count(window(history, 6))
    summ = count([summary] + history[-4:]) if turn > 4 else full
    totals["full"] += full
    totals["window"] += win
    totals["summary"] += summ
    if turn <= 10 or turn % 5 == 0:
        print(f"{turn:>5} {full:>8} {win:>8} {summ:>8}")
    history.append(answer)

print(f"\n{'Σύνολο':>5} {totals['full']:>8} {totals['window']:>8} {totals['summary']:>8}")
label = " (εκτίμηση τιμής)" if estimated else ""
print(f"$ ανά 1.000 συνομιλίες{label}: full {totals['full'] * cost_in * 1000:.2f} | window {totals['window'] * cost_in * 1000:.2f} | summary {totals['summary'] * cost_in * 1000:.2f}")
