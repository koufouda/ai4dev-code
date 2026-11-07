"""Διάλεξη 16: fallback. Αν το βασικό μοντέλο πέσει, απαντά το εφεδρικό.

Για το demo, το «βασικό» είναι ένα μοντέλο που δεν υπάρχει: αποτυγχάνει πάντα.

Χρήση:  python fallback_demo.py
"""
import time
from pythia_arch import call_with_fallback, MODEL, MODEL_LOCAL

messages = [{"role": "user", "content": "Πες μια σύντομη καλημέρα σε έναν πελάτη ενός καφέ."}]
scenarios = [
    ("Κανονικά", [MODEL, MODEL_LOCAL]),
    ("Το βασικό πέφτει", ["anthropic/claude-model-pou-den-yparxei", MODEL_LOCAL]),
    ("Πέφτουν όλα", ["anthropic/claude-model-pou-den-yparxei", "ollama_chat/kai-auto-den-yparxei"]),
]
for title, models in scenarios:
    print(f"\n=== {title}: {models} ===")
    start = time.perf_counter()
    try:
        resp, used, errors = call_with_fallback(messages, models)
        print(f"Απάντησε: {used} ({time.perf_counter() - start:.1f}s)  Απέτυχαν: {errors or 'κανένα'}")
        print("→", resp.choices[0].message.content.strip()[:100])
    except RuntimeError as e:
        print(f"Σφάλμα ({time.perf_counter() - start:.1f}s): {e}")
