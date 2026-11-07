"""Διάλεξη 1: πόσα tokens «κοστίζει» το ίδιο νόημα στα ελληνικά και στα αγγλικά.

Χρήση:  python tokens.py              (σύγκριση προτάσεων)
        python tokens.py Θεσσαλονίκη  (πώς κόβεται μια λέξη)
"""
import sys
import tiktoken

PAIRS = [
    ("Η τεχνητή νοημοσύνη αλλάζει τον τρόπο που γράφουμε λογισμικό.", "Artificial intelligence is changing the way we write software."),
    ("Καλημέρα σας, θα ήθελα να κλείσω ένα ραντεβού για την Πέμπτη.", "Good morning, I would like to book an appointment for Thursday."),
]

if len(sys.argv) > 1:
    enc = tiktoken.get_encoding("o200k_base")
    for word in sys.argv[1:]:
        token_ids = enc.encode(" " + word)
        pieces = []
        for t in token_ids:
            pieces.append(enc.decode([t]))
        print(f"{word} -> {len(pieces)} tokens: {' | '.join(pieces)}")
    sys.exit()

for number, (greek, english) in enumerate(PAIRS, start=1):
    print(f"{number}. {greek}\n   {english}")

for name in ["cl100k_base", "o200k_base"]:
    enc = tiktoken.get_encoding(name)
    print(f"\n{name}")
    for number, (greek, english) in enumerate(PAIRS, start=1):
        g = len(enc.encode(greek))
        e = len(enc.encode(english))
        print(f"  {number}. ΕΛ {g:3} tokens | EN {e:3} tokens | τα ελληνικά θέλουν x{g / e:.1f}")
