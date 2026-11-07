"""Εβδομάδα 10, διάλεξη 20: κοινές συναρτήσεις για τη σύγκριση μοντέλων (cloud και τοπικά, μέσω LiteLLM)."""
import json
import time
import urllib.request
from pythia_rag import completion, safe_cost

OLLAMA = "http://localhost:11434"

def read_models(path="models.txt"):
    lines = [line.strip() for line in open(path, encoding="utf-8")]
    return [line for line in lines if line and not line.startswith("#")]

def is_local(model):
    return model.startswith("ollama")

def ask(model, prompt, tools=None):
    start = time.perf_counter()
    try:
        extra = {"tools": tools} if tools else {}
        resp = completion(model=model, messages=[{"role": "user", "content": prompt}], timeout=180, num_retries=1, **extra)
    except Exception as e:
        return "", time.perf_counter() - start, 0.0, f"{type(e).__name__}: {str(e).splitlines()[0][:80]}"
    seconds = time.perf_counter() - start
    msg = resp.choices[0].message
    out = msg.tool_calls[0].function.name if msg.tool_calls else (msg.content or "")
    cost = 0.0 if is_local(model) else safe_cost(resp, model)
    return out, seconds, cost, None

def ollama_show(name):
    req = urllib.request.Request(OLLAMA + "/api/show", data=json.dumps({"model": name}).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=10))

def ollama_list():
    return json.load(urllib.request.urlopen(OLLAMA + "/api/tags", timeout=5))["models"]
