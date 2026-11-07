"""Διάλεξη 20: πόσο γρήγορα απαντά κάθε μοντέλο; Χρόνος μέχρι την πρώτη λέξη, συνολικός χρόνος, tokens ανά δευτερόλεπτο.

Χρήση:  python speed_test.py                  (τα μοντέλα του models.txt)
        python speed_test.py ollama_chat/gemma3:4b
"""
import sys
import time
from litellm import completion, token_counter
from pythia_models import read_models

PROMPT = "Εξήγησε σε 5 προτάσεις, στα ελληνικά, πώς φτιάχνεται ένας καλός espresso."
models = sys.argv[1:] or read_models()
print(f"{'μοντέλο':<34}{'1η λέξη':>9}{'σύνολο':>9}{'tokens':>8}{'tok/s':>8}")
for model in models:
    start = time.perf_counter()
    first = None
    text = ""
    try:
        for chunk in completion(model=model, messages=[{"role": "user", "content": PROMPT}], stream=True, timeout=180):
            piece = chunk.choices[0].delta.content or ""
            if piece and first is None:
                first = time.perf_counter() - start
            text += piece
    except Exception as e:
        print(f"{model:<34}  σφάλμα: {type(e).__name__}: {str(e).splitlines()[0][:60]}")
        continue
    total = time.perf_counter() - start
    tokens = token_counter(model="gpt-3.5-turbo", text=text)
    rate = tokens / (total - (first or 0)) if total > (first or 0) else 0
    print(f"{model:<34}{first or 0:>8.1f}s{total:>8.1f}s{tokens:>8}{rate:>8.0f}")
print("\nΠΡΟΣΟΧΗ: η πρώτη κλήση σε τοπικό μοντέλο περιλαμβάνει και το φόρτωμα στη μνήμη. Τρέξτε δύο φορές.")
