"""Εβδομάδα 6, διάλεξη 11: κοινές συναρτήσεις για μνήμη, tokens και κόστος.

Το χρησιμοποιούν τα chat_memory.py, cache_demo.py, context_limit.py, growth.py και app_chat.py.
"""
import csv
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
from litellm import completion, completion_cost, token_counter, get_model_info

MODEL = os.getenv("MODEL", "anthropic/claude-haiku-5-5")
MODEL_LOCAL = os.getenv("MODEL_LOCAL", "ollama_chat/gemma3:4b")
SYSTEM = {"role": "system", "content": "Είσαι η Πυθία, βοηθός του e-shop «Μπρίκι». Απαντάς σύντομα, σε 2-3 προτάσεις, στα ελληνικά."}
COST_FILE = "costs.csv"

def price(model):
    try:
        info = get_model_info(model)
        cost_in = info["input_cost_per_token"]
        cost_out = info["output_cost_per_token"]
    except Exception:
        cost_in, cost_out = 0, 0
    if model.startswith("ollama"):
        return 0.0, 0.0, False
    if not cost_in:
        return 1 / 1_000_000, 5 / 1_000_000, True
    return cost_in, cost_out, False

def usage(resp, model):
    u = resp.usage
    cache_write = getattr(u, "cache_creation_input_tokens", 0) or 0
    details = getattr(u, "prompt_tokens_details", None)
    cache_read = (getattr(details, "cached_tokens", 0) or 0) if details else 0
    try:
        cost = completion_cost(completion_response=resp)
    except Exception:
        cost = 0.0
    if not cost:
        cost_in, cost_out, _ = price(model)
        plain = max(0, u.prompt_tokens - cache_write - cache_read)
        cost = plain * cost_in + cache_write * cost_in * 1.25 + cache_read * cost_in * 0.1 + u.completion_tokens * cost_out
    return {"input": u.prompt_tokens, "output": u.completion_tokens, "cache_write": cache_write, "cache_read": cache_read, "cost": cost}

def log_cost(script, model, numbers, seconds):
    new_file = not os.path.exists(COST_FILE)
    with open(COST_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["time", "script", "model", "input", "output", "cache_write", "cache_read", "cost", "seconds"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), script, model, numbers["input"], numbers["output"], numbers["cache_write"], numbers["cache_read"], f"{numbers['cost']:.6f}", f"{seconds:.2f}"])

def ask(messages, model=MODEL, script="?", **extra):
    start = time.perf_counter()
    resp = completion(model=model, messages=messages, num_retries=3, **extra)
    seconds = time.perf_counter() - start
    numbers = usage(resp, model)
    log_cost(script, model, numbers, seconds)
    answer = resp.choices[0].message.content
    return answer, numbers, seconds

def count(messages, model=MODEL):
    return token_counter(model=model, messages=messages)

def window(history, n=6):
    recent = history[1:][-n:]
    if recent and recent[0]["role"] == "assistant":
        recent = recent[1:]
    return [history[0]] + recent

def summarize(history, model=MODEL, keep=4):
    old = history[1:-keep]
    recent = history[-keep:]
    if not old:
        return history, 0.0
    text = "\n".join(m["role"] + ": " + m["content"] for m in old)
    request = ("Συνόψισε τη συνομιλία σε λίγες γραμμές. Κράτα ονόματα, αριθμούς, αποφάσεις "
               "και ό,τι ζήτησε ο χρήστης.\n\n<conversation>\n" + text + "\n</conversation>")
    summary, numbers, _ = ask([{"role": "user", "content": request}], model, "summary")
    base = history[0]["content"].split("\n\nΣύνοψη της συνομιλίας ως τώρα:")[0]
    note = {"role": "system", "content": base + "\n\nΣύνοψη της συνομιλίας ως τώρα:\n" + summary}
    return [note] + recent, numbers["cost"]

def option(argv, name, default):
    if name in argv:
        return argv[argv.index(name) + 1]
    return default
