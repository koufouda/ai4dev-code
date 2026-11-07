"""Διάλεξη 11: η Πυθία συνομιλεί με τρεις στρατηγικές μνήμης. Δείχνει tokens και κόστος σε κάθε γύρο.

Χρήση:  python chat_memory.py                       (full: όλο το ιστορικό, γράφετε εσείς)
        python chat_memory.py --auto                (οι ερωτήσεις από το conversation.txt)
        python chat_memory.py --auto --strategy window
        python chat_memory.py --auto --strategy summary
        python chat_memory.py --budget 0.01         (σταματά όταν το κόστος ξεπεράσει το όριο)
        python chat_memory.py --local               (τοπικό μοντέλο)
Γράψτε «τέλος» για έξοδο.
"""
import sys
from pythia_memory import MODEL, MODEL_LOCAL, SYSTEM, ask, window, summarize, option

strategy = option(sys.argv, "--strategy", "full")
budget = float(option(sys.argv, "--budget", "0.10"))
auto = "--auto" in sys.argv
model = MODEL_LOCAL if "--local" in sys.argv else MODEL
lines = open("conversation.txt", encoding="utf-8").read().splitlines() if auto else []

history = [SYSTEM]
total = 0.0
turn = 0
print(f"Στρατηγική: {strategy} | μοντέλο: {model} | όριο ${budget}\n")

while True:
    if auto:
        if not lines:
            break
        question = lines.pop(0)
        print("Εσύ:", question)
    else:
        question = input("Εσύ: ")
        if question == "τέλος":
            break
    history.append({"role": "user", "content": question})
    messages = window(history, 6) if strategy == "window" else history
    answer, numbers, seconds = ask(messages, model, "chat_memory")
    history.append({"role": "assistant", "content": answer})
    if strategy == "summary" and len(history) > 9:
        history, summary_cost = summarize(history, model)
        total += summary_cost
        print("   (τα παλιά μηνύματα έγιναν σύνοψη)")
    turn += 1
    total += numbers["cost"]
    print("Πυθία:", answer)
    print(f"   [γύρος {turn}] είσοδος {numbers['input']} | έξοδος {numbers['output']} | ${numbers['cost']:.5f} | σύνολο ${total:.5f} | στάλθηκαν {len(messages)} μηνύματα\n")
    if total > budget:
        print(f"Σταματώ: το κόστος ${total:.4f} ξεπέρασε το όριο ${budget}.")
        break
