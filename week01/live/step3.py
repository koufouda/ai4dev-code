"""Βήμα 3: χρόνος και κόστος. Στο βήμα 4 αλλάζετε μόνο τη γραμμή MODEL."""
import time
from dotenv import load_dotenv
load_dotenv()
from litellm import completion, completion_cost

MODEL = "anthropic/claude-haiku-5-5"
QUESTION = "Ποια είναι η πρωτεύουσα της Κρήτης;"

start = time.perf_counter()
message = {"role": "user", "content": QUESTION}
resp = completion(model=MODEL, messages=[message])
seconds = time.perf_counter() - start
print(resp.choices[0].message.content)

try:
    cost = completion_cost(completion_response=resp)
except Exception:
    cost = 0.0

out_tokens = resp.usage.completion_tokens
print(f"\n{seconds:.1f}s | {out_tokens} tokens απάντησης | ${cost:.6f}")
