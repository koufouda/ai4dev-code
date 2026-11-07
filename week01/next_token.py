"""Διάλεξη 1: τι «σκέφτεται» το μοντέλο για την επόμενη λέξη.

Δείχνει, για κάθε token που γράφει το μοντέλο, τις 10 πιθανότερες επιλογές με τις πιθανότητές τους.
Χρειάζεται μοντέλο που επιστρέφει logprobs (π.χ. OpenAI). Χρήση:
    python next_token.py "Το πρωί πίνω έναν"
    python next_token.py --max_tokens 3 "Το πρωί πίνω έναν"
    python next_token.py --max_tokens 3 --temperature 1.5 "Το πρωί πίνω έναν"
"""
import math
import os
import sys
from dotenv import load_dotenv

load_dotenv()
from litellm import completion

model = os.getenv("MODEL_LOGPROBS", "openai/gpt-4.1-mini")
args = sys.argv[1:]
max_tokens = 1
if "--max_tokens" in args:
    i = args.index("--max_tokens")
    max_tokens = int(args[i + 1])
    del args[i:i + 2]

settings = {"max_tokens": max_tokens, "logprobs": True, "top_logprobs": 10}
if "--temperature" in args:
    i = args.index("--temperature")
    settings["temperature"] = float(args[i + 1])
    del args[i:i + 2]

prompt = " ".join(args)
if prompt == "":
    prompt = "Το πρωί πίνω έναν"

system_message = {"role": "system", "content": "Συνέχισε το κείμενο του χρήστη. Γράψε μόνο τη συνέχεια."}
user_message = {"role": "user", "content": prompt}

try:
    resp = completion(model=model, messages=[system_message, user_message], **settings)
except Exception as e:
    sys.exit("Δεν πήρα απάντηση: " + type(e).__name__ + ": " + str(e).splitlines()[0][:200])

positions = resp.choices[0].logprobs.content
print("[temperature: " + str(settings.get("temperature", "προεπιλογή του μοντέλου")) + "]")
print(f'"{prompt}" + "{resp.choices[0].message.content}"')

for number, position in enumerate(positions, start=1):
    print(f"\nToken {number}: διάλεξε {position.token!r}")
    for alt in position.top_logprobs:
        percent = math.exp(alt.logprob) * 100
        bar = "#" * round(percent / 2)
        print(f"{percent:9.5f}%  {bar:50} {alt.token!r}")
