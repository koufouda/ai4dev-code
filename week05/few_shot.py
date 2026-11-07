"""Διάλεξη 9: zero-shot ή few-shot; Ίδια κατάταξη, με και χωρίς παραδείγματα.

Χρήση:  python few_shot.py
"""
import os
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
messages_to_classify = [
    "Η μηχανή στάζει νερό από κάτω.",
    "Θέλω τιμολόγιο αντί για απόδειξη.",
    "Μου ήρθε λάθος χρώμα, θέλω να το αλλάξω.",
    "Πότε θα έχετε ξανά τις κάψουλες βανίλια;",
    "Περιμένω δέκα μέρες, είστε απαράδεκτοι!",
]

zero = "Σε ποια κατηγορία ανήκει το μήνυμα; Απάντησε με μία λέξη ή φράση.\n\nΜήνυμα: "
few = (
    "Σε ποια κατηγορία ανήκει το μήνυμα; Απάντησε ΜΟΝΟ με την κατηγορία.\n\n"
    "Μήνυμα: Το μηχάνημα δεν ανάβει.\nΚατηγορία: τεχνικό πρόβλημα\n\n"
    "Μήνυμα: Με χρεώσατε δύο φορές.\nΚατηγορία: τιμολόγηση\n\n"
    "Μήνυμα: Έχετε σε άλλο μέγεθος;\nΚατηγορία: άλλο\n\n"
    "Μήνυμα: "
)

print(f"{'Μήνυμα':<45} {'Zero-shot':<28} Few-shot")
for text in messages_to_classify:
    a = completion(model=model, messages=[{"role": "user", "content": zero + text}], num_retries=3)
    b = completion(model=model, messages=[{"role": "user", "content": few + text + "\nΚατηγορία:"}], num_retries=3)
    label_a = a.choices[0].message.content.strip()[:27]
    label_b = b.choices[0].message.content.strip()[:27]
    print(f"{text[:44]:<45} {label_a:<28} {label_b}")
