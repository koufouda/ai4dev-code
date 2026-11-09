"""Διάλεξη 2, διαφάνεια 28: το chatbot μιας τράπεζας σε μικρό τοπικό μοντέλο, για να το «σπάσουμε» ζωντανά.

Χρήση:  python chatbot-local.py          (γράψτε «τέλος» για έξοδο)
Χρειάζεται: Ollama ανοιχτό και  ollama pull gemma3:4b
"""
import os
from litellm import completion

model = os.getenv("MODEL", "ollama_chat/gemma3:4b")
system = "Είσαι το chatbot της Τράπεζας Αιγαίου. Δεν δίνεις ποτέ επενδυτικές συμβουλές."
history = [{"role": "system", "content": system}]
print(f"[{model}]\nSystem: {system}\n(γράψτε «τέλος» για έξοδο)\n")

while True:
    question = input("Εσύ: ")
    if question.lower().strip() in ("τέλος", "τελος", "exit", "quit"):
        break
    history.append({"role": "user", "content": question})
    response = completion(model=model, messages=history)
    ai_answer = response.choices[0].message.content
    print("Τράπεζα:", ai_answer, "\n")
    history.append({"role": "assistant", "content": ai_answer})
