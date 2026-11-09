"""Διάλεξη 2: chatbot με μνήμη, που δείχνει μετά από κάθε απάντηση tokens, χρόνο και κόστος.

Χρήση:  python chatbot.py            (γράψτε «τέλος» για έξοδο)
        set MODEL=ollama_chat/gemma3:4b   και μετά  python chatbot.py   (τοπικό μοντέλο, cmd)
"""
import os
import time
from dotenv import load_dotenv

load_dotenv()
from litellm import completion, completion_cost, get_model_info

model = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
history = [{"role": "system", "content": "Είσαι σύντομος και ευγενικός βοηθός. Απαντάς πάντα στα Ελληνικά."}]

while True:
    question = input("Εσύ: ")
    if question.lower().strip() in ("τέλος", "τελος", "exit", "quit"):
        break

    history.append({"role": "user", "content": question})
    start = time.perf_counter()
    response = completion(model=model, messages=history, num_retries=3)
    elapsed = time.perf_counter() - start
    ai_answer = response.choices[0].message.content
    print("AI:", ai_answer)
    history.append({"role": "assistant", "content": ai_answer})

    u = response.usage
    cd = u.completion_tokens_details
    pd = u.prompt_tokens_details
    print("\n--------\nΕίσοδος:", u.prompt_tokens)
    print("Έξοδος:", u.completion_tokens)
    print("  από αυτά «σκέψη»:", cd.reasoning_tokens if cd else "—")
    print("  από αυτά κείμενο:", cd.text_tokens if cd else "—")
    print("Από cache (φθηνότερα):", pd.cached_tokens if pd else "—")
    print("Γράφτηκαν στην cache:", getattr(u, "cache_creation_input_tokens", "—"))

    try:
        cost = completion_cost(completion_response=response)
        info = get_model_info(model)
        print(f"Τιμή εισόδου: ${info['input_cost_per_token'] * 1_000_000:.2f} ανά 1 εκατ. tokens")
        print(f"Τιμή εξόδου:  ${info['output_cost_per_token'] * 1_000_000:.2f} ανά 1 εκατ. tokens")
    except Exception:
        cost = 0.0
    print(f"[{model}] {elapsed:.1f}s | tokens: {u.prompt_tokens} in + {u.completion_tokens} out | ${cost:.6f}\n--------\n")
