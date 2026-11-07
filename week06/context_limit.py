"""Διάλεξη 11: τι γίνεται όταν το κείμενο δεν χωράει στο context του τοπικού μοντέλου.

Το Ollama, αν δεν του πείτε αλλιώς, διαβάζει μόνο ένα κομμάτι του κειμένου (π.χ. 4.096 tokens)
και κόβει την αρχή ΧΩΡΙΣ σφάλμα. Ρωτάμε για το πρώτο προϊόν του καταλόγου, που κόβεται.

Χρήση:  python context_limit.py
        python context_limit.py --ctx 16384     (μεγαλύτερο context: θέλει περισσότερη μνήμη RAM)
"""
import sys
from pythia_memory import MODEL_LOCAL, ask, count, option

catalog = open("katalogos.txt", encoding="utf-8").read()
question = "Πόσο κοστίζει το προϊόν με κωδικό ΜΠ-001; Απάντησε μόνο με την τιμή."
messages = [{"role": "user", "content": "<katalogos>\n" + catalog + "\n</katalogos>\n\n" + question}]
extra = {}
if "--ctx" in sys.argv:
    extra["num_ctx"] = int(option(sys.argv, "--ctx", "16384"))

sent = count(messages, MODEL_LOCAL)
answer, numbers, seconds = ask(messages, MODEL_LOCAL, "context_limit", **extra)
read = numbers["input"]

print(f"Στείλαμε περίπου {sent} tokens. Το μοντέλο διάβασε {read}. ({seconds:.1f}s)")
print(f"Απάντηση: {answer.strip()}   (σωστό: 349.00 €)")
if read < sent * 0.8:
    print("→ Το κείμενο δεν χώρεσε. Η αρχή του κόπηκε χωρίς κανένα σφάλμα, άρα το μοντέλο δεν είδε την ΜΠ-001.")
