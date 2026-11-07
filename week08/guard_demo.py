"""Διάλεξη 16: guardrail εισόδου. Τα προσωπικά δεδομένα κρύβονται ΠΡΙΝ φύγουν προς το μοντέλο.

Χρήση:  python guard_demo.py
        python guard_demo.py "Η κάρτα μου 4111 1111 1111 1111 χρεώθηκε δύο φορές"
"""
import sys
from pythia_arch import guard_input

messages = sys.argv[1:] or [
    "Η κάρτα μου 4111 1111 1111 1111 χρεώθηκε δύο φορές για την παραγγελία 48213",
    "Πάρτε με τηλέφωνο στο 6912345678 ή στείλτε στο maria.p@example.com",
    "Θέλω τιμολόγιο, ΑΦΜ 123456789",
    "Πόσους μήνες εγγύηση έχει η ΜΠ-001;",
]
for m in messages:
    clean, found = guard_input(m)
    print(f"Πριν:  {m}\nΜετά:  {clean}\n       βρέθηκαν: {found or 'τίποτα'}\n")
