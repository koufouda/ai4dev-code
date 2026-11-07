"""Διάλεξη 11, άνοιγμα: το μοντέλο δεν θυμάται τίποτα. Η «μνήμη» είναι δική μας δουλειά.

Χρήση:  python forget.py
"""
from pythia_memory import ask, SYSTEM

first = {"role": "user", "content": "Γεια, με λένε Μαρία και έχω τη μηχανή ΜΠ-001."}
second = {"role": "user", "content": "Πώς με λένε και ποια μηχανή έχω;"}

print("===== Δύο χωριστές κλήσεις =====")
answer, numbers, _ = ask([SYSTEM, first], script="forget")
print("Πυθία:", answer)
answer, numbers, _ = ask([SYSTEM, second], script="forget")
print("Πυθία:", answer, f"   [είσοδος {numbers['input']} tokens]")

print("\n===== Με ιστορικό =====")
reply, _, _ = ask([SYSTEM, first], script="forget")
history = [SYSTEM, first, {"role": "assistant", "content": reply}, second]
answer, numbers, _ = ask(history, script="forget")
print("Πυθία:", answer, f"   [είσοδος {numbers['input']} tokens]")
