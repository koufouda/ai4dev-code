"""Διάλεξη 10: το σύνολο δοκιμών ως κανονικά tests του pytest.

Χρήση:  pytest -v test_tickets.py
Κάθε test καλεί το μοντέλο, άρα κοστίζει λίγο και χρειάζεται δίκτυο.
"""
import json
import pytest
from pythia_ticket import extract_ticket

CASES = json.load(open("eval_cases.json", encoding="utf-8"))

@pytest.mark.parametrize("case", CASES, ids=[c["file"] for c in CASES])
def test_ticket(case):
    text = open(case["file"], encoding="utf-8").read()
    ticket, _, _ = extract_ticket(text)
    assert ticket.category == case["category"]
    assert ticket.order_number == case["order_number"]
