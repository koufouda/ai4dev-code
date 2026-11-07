"""Διάλεξη 18: ReAct «με το χέρι», όπως στο άρθρο του 2022. Χωρίς tool calling: μόνο κείμενο και ένα regex.

Το μοντέλο γράφει «Σκέψη: …» και «Ενέργεια: εργαλείο[όρισμα]». Εμείς τρέχουμε το εργαλείο και γράφουμε «Παρατήρηση: …».
Έτσι φαίνεται ότι ένας agent είναι απλώς ένας βρόχος γύρω από κλήσεις σε μοντέλο.

Χρήση:  python react_text.py
        python react_text.py "Πόσο κάνουν 2 ΜΠ-012 μαζί με μία ΜΠ-001;"
"""
import sys
import re
from pythia_rag import MODEL, completion
from pythia_tools import FUNCTIONS

SYSTEM = """Είσαι η Πυθία του e-shop «Μπρίκι». Λύνεις την εργασία σε βήματα, ΑΚΡΙΒΩΣ με αυτή τη μορφή:
Σκέψη: τι θέλω να μάθω και γιατί
Ενέργεια: όνομα_εργαλείου[όρισμα]
Μετά σταματάς και περιμένεις την «Παρατήρηση:» που θα σου δώσω. Όταν ξέρεις την απάντηση, γράφεις:
Τελική απάντηση: η απάντηση στα ελληνικά
Εργαλεία: get_order[αριθμός παραγγελίας], get_product[κωδικός], find_products[λέξη], search_docs[ερώτημα], calculate[έκφραση], today[]"""

task = sys.argv[1] if len(sys.argv) > 1 else "Η παραγγελία 48213: τι προϊόν είναι και πόσο θα κόστιζε αν αγόραζα άλλα δύο ίδια;"
messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]
for step in range(1, 7):
    resp = completion(model=MODEL, messages=messages, stop=["Παρατήρηση:"], num_retries=3)
    text = resp.choices[0].message.content.strip()
    print(f"--- βήμα {step} ---\n{text}")
    if "Τελική απάντηση:" in text:
        break
    action = re.search(r"Ενέργεια:\s*(\w+)\[(.*?)\]", text)
    if not action:
        observation = "Δεν βρήκα «Ενέργεια: εργαλείο[όρισμα]». Γράψε μία ενέργεια ή την τελική απάντηση."
    elif action.group(1) not in FUNCTIONS:
        observation = f"Δεν υπάρχει εργαλείο {action.group(1)}."
    else:
        func = FUNCTIONS[action.group(1)]
        observation = str(func(action.group(2)) if action.group(2) else func())
    print(f"Παρατήρηση: {' '.join(observation.split())[:150]}")
    messages.append({"role": "assistant", "content": text})
    messages.append({"role": "user", "content": "Παρατήρηση: " + observation})
