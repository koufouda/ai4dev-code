"""Διάλεξη 18: προσθέτουμε δικό μας εργαλείο, χωρίς να αλλάξουμε το pythia_tools.py. Πρότυπο για το project σας.

Τρία βήματα: 1. η συνάρτηση, 2. το σχήμα (περιγραφή!), 3. καταχώριση στο FUNCTIONS.

Χρήση:  python extra_tool.py
        python extra_tool.py "Πόσα μεταφορικά πληρώνω για 2 ΜΠ-004 στην Κρήτη;"
"""
import sys
from pythia_tools import TOOLS, FUNCTIONS
from pythia_agent import agent

def shipping_cost(total, area):
    if float(total) > 50:
        return "0.00 € (δωρεάν αποστολή για παραγγελίες άνω των 50 €)"
    price = 6.50 if area.lower() in ("νησιά", "κρήτη", "νησι") else 3.90
    return f"{price:.2f} €"

SHIPPING = {"type": "function", "function": {
    "name": "shipping_cost",
    "description": "Κόστος αποστολής για ένα σύνολο παραγγελίας και μια περιοχή. Χρησιμοποίησέ το για ερωτήσεις για μεταφορικά.",
    "parameters": {"type": "object", "properties": {
        "total": {"type": "number", "description": "Σύνολο παραγγελίας σε ευρώ"},
        "area": {"type": "string", "description": "«ηπειρωτική» ή «νησιά» (η Κρήτη μετρά ως νησιά)"}},
        "required": ["total", "area"]}}}

FUNCTIONS["shipping_cost"] = shipping_cost

task = sys.argv[1] if len(sys.argv) > 1 else "Πόσα μεταφορικά πληρώνω για 2 συσκευασίες ΜΠ-004 στην Κρήτη;"
r = agent(task, tools=TOOLS + [SHIPPING])
print(f"\n   [{len(r['steps'])} ενέργειες | ${r['cost']:.5f}]")
