"""Διάλεξη 2, τελικό demo: «τυφλή» σύγκριση μοντέλων.

Η ίδια ερώτηση πηγαίνει σε όλα τα μοντέλα του ARENA_MODELS. Οι απαντήσεις
εμφανίζονται ως Α, Β, Γ... με τυχαία σειρά. Η τάξη ψηφίζει και μετά
αποκαλύπτουμε ποιο μοντέλο ήταν ποιο, πόσο άργησε και πόσο κόστισε.
Χρήση:  python arena.py "Εξήγησε τι είναι το RAG σε ένα παιδί 10 χρονών."
"""
import os
import random
import sys
import time
from dotenv import load_dotenv

load_dotenv()
from litellm import completion, completion_cost

question = " ".join(sys.argv[1:])
if question == "":
    question = "Εξήγησε τι είναι ένα LLM σε έναν παππού από την Κρήτη, σε 3 προτάσεις."

models_text = os.getenv("ARENA_MODELS", "anthropic/claude-haiku-5-5,ollama_chat/gemma3:4b")
models = models_text.split(",")
random.shuffle(models)
labels = ["Α", "Β", "Γ", "Δ", "Ε", "Ζ"]
results = []

for i in range(len(models)):
    model = models[i].strip()
    label = labels[i]
    message = {"role": "user", "content": question}
    start = time.perf_counter()
    try:
        resp = completion(model=model, messages=[message], timeout=120, num_retries=3)
        answer = resp.choices[0].message.content
    except Exception as e:
        answer = "(σφάλμα: " + type(e).__name__ + ")"
        resp = None
    seconds = time.perf_counter() - start
    cost = 0.0
    if resp is not None:
        try:
            cost = completion_cost(completion_response=resp)
        except Exception:
            cost = 0.0
    results.append({"label": label, "model": model, "seconds": seconds, "cost": cost})
    print(f"\n===== Μοντέλο {label} =====")
    print(answer)

input("\nΨηφίστε! Πατήστε Enter για αποκάλυψη...")
for r in results:
    print(f"{r['label']} = {r['model']:35} {r['seconds']:5.1f}s  ${r['cost']:.6f}")
