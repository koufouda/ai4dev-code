"""Διάλεξη 2: streaming. Το κείμενο εμφανίζεται καθώς παράγεται.

Χρήση:  python stream.py "Γράψε μια σύντομη ιστορία για τον Τάλω."
        python stream.py --local "..."
"""
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

args = sys.argv[1:]
if "--local" in args:
    args.remove("--local")
    model = os.getenv("MODEL_LOCAL", "ollama_chat/gemma3:4b")
else:
    model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")

prompt = " ".join(args)
if prompt == "":
    prompt = "Γράψε μια ιστορία 150 λέξεων για τον Τάλω, τον χάλκινο γίγαντα της Κρήτης."

message = {"role": "user", "content": prompt}
start = time.perf_counter()
first = None
stream = completion(model=model, messages=[message], stream=True, num_retries=3)

for chunk in stream:
    text = chunk.choices[0].delta.content
    if text is None:
        continue
    if first is None:
        first = time.perf_counter() - start
    print(text, end="", flush=True)

total = time.perf_counter() - start
if first is None:
    first = 0.0
print(f"\n\n[{model}] πρώτη λέξη σε {first:.2f}s, ολόκληρη απάντηση σε {total:.2f}s")
