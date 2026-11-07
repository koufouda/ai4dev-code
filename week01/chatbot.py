"""Διάλεξη 1, τελικό demo: ένα chatbot με μνήμη. Γράψτε 'τέλος' για έξοδο."""
import os
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
history = [{"role": "system", "content": "Είσαι σύντομος και ευγενικός βοηθός. Απαντάς στα ελληνικά."}]

while True:
    question = input("Εσύ: ")
    if question == "τέλος":
        break
    history.append({"role": "user", "content": question})
    resp = completion(model=model, messages=history, num_retries=3)
    answer = resp.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    print("AI:", answer)
