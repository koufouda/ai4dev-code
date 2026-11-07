"""Διάλεξη 2: η πρώτη κλήση. Μία ερώτηση, μία απάντηση, και τι κόστισε.

Χρήση:  python ask.py "Ποια είναι η πρωτεύουσα της Κρήτης;"
        python ask.py --local "..."   (τοπικό μοντέλο μέσω Ollama)
"""
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()
from litellm import completion, completion_cost

args = sys.argv[1:]

if "--local" in args:
    args.remove("--local")
    model = os.getenv("MODEL_LOCAL", "ollama_chat/gemma3:4b")
else:
    model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")

question = " ".join(args)
if question == "":
    question = "Πες μου ένα ενδιαφέρον γεγονός για την Κρήτη."

message = {"role": "user", "content": question}
start = time.perf_counter()
resp = completion(model=model, messages=[message], num_retries=3)
seconds = time.perf_counter() - start

print(resp.choices[0].message.content)

try:
    cost = completion_cost(completion_response=resp)
except Exception:
    cost = 0.0

tokens_in = resp.usage.prompt_tokens
tokens_out = resp.usage.completion_tokens
print(f"\n[{model}] {seconds:.1f}s | tokens: {tokens_in} in + {tokens_out} out | ${cost:.6f}")
