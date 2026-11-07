"""Εβδομάδα 8, διάλεξη 16: μοτίβα αρχιτεκτονικής. Router, κλασικός κώδικας, fallback, cache, guardrails, pipeline.

Χτίζει πάνω στα pythia_rag.py (εβδομάδα 7) και pythia_safe.py (διάλεξη 15).
"""
import json
import os
import re
import time
from typing import Literal
from pydantic import BaseModel, Field
from pythia_rag import MODEL, completion, safe_cost, normalize, embed, cosine
from pythia_safe import ask_safe, output_guard

MODEL_LOCAL = os.getenv("MODEL_LOCAL", "ollama_chat/gemma3:4b")
CACHE_FILE = "cache.json"

class Route(BaseModel):
    route: Literal["order_status", "documents", "complaint", "human", "chitchat"] = Field(description=(
        "order_status: ρωτά πού είναι η παραγγελία του · documents: ερώτηση για προϊόντα, εγγύηση, όρους, επιστροφές, απόρρητο · "
        "complaint: παράπονο ή πρόβλημα που θέλει ticket · human: ζητά άνθρωπο ή είναι πολύ θυμωμένος · chitchat: χαιρετισμός, ευχαριστώ"))
    reason: str = Field(description="Αιτιολόγηση σε μία πρόταση")

def route_rules(question):
    q = normalize(question)
    if re.search(r"\b\d{5}\b", q) and "παραγγελ" in q:
        return "order_status"
    if re.search(r"θελω (να μιλησω με )?(ανθρωπο|υπαλληλο)|εκπροσωπο", q):
        return "human"
    return None

def route_llm(question, model=MODEL):
    messages = [{"role": "user", "content": "Διάλεξε πού πηγαίνει το μήνυμα του πελάτη ενός e-shop με μηχανές καφέ.\n<message>" + question + "</message>"}]
    resp = completion(model=model, messages=messages, response_format=Route, num_retries=3)
    return Route.model_validate_json(resp.choices[0].message.content), safe_cost(resp, model)

def route(question):
    r = route_rules(question)
    if r:
        return r, "κανόνας", 0.0
    decision, cost = route_llm(question)
    return decision.route, "LLM: " + decision.reason, cost

def order_status(question):
    match = re.search(r"\b\d{5}\b", question)
    orders = json.load(open("orders.json", encoding="utf-8"))
    if not match or match.group() not in orders:
        return "Δεν βρίσκω αυτή την παραγγελία. Ελέγξτε τον πενταψήφιο αριθμό στο email επιβεβαίωσης."
    o = orders[match.group()]
    return f"Η παραγγελία {match.group()} είναι «{o['status']}». Εκτιμώμενη παράδοση: {o['eta']}."

def call_with_fallback(messages, models=None, timeout=30):
    models = models or [MODEL, MODEL_LOCAL]
    errors = []
    for m in models:
        try:
            resp = completion(model=m, messages=messages, num_retries=1, timeout=timeout)
            return resp, m, errors
        except Exception as e:
            errors.append(f"{m}: {type(e).__name__}")
    raise RuntimeError("Όλα τα μοντέλα απέτυχαν: " + "; ".join(errors))

def cache_load():
    if os.path.exists(CACHE_FILE):
        return json.load(open(CACHE_FILE, encoding="utf-8"))
    return []

def cache_get(question, similarity=0.92):
    cache = cache_load()
    key = " ".join(normalize(question).split())
    for item in cache:
        if item["key"] == key:
            return item["answer"], "exact"
    if not cache:
        return None, None
    v = embed([question])[0]
    best = max(cache, key=lambda item: cosine(v, item["vector"]))
    if cosine(v, best["vector"]) >= similarity:
        return best["answer"], f"semantic ({cosine(v, best['vector']):.2f}, «{best['question']}»)"
    return None, None

def cache_put(question, answer):
    cache = cache_load()
    cache.append({"question": question, "key": " ".join(normalize(question).split()), "vector": embed([question])[0], "answer": answer})
    json.dump(cache, open(CACHE_FILE, "w", encoding="utf-8"), ensure_ascii=False)

PII = [
    (r"\b\d(?:[ -]?\d){12,18}\b", "[ΚΑΡΤΑ]"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+", "[EMAIL]"),
    (r"(?:\+30\s?)?\b(?:69\d{8}|2\d{9})\b", "[ΤΗΛΕΦΩΝΟ]"),
    (r"\bΑΦΜ:?\s*\d{9}\b", "ΑΦΜ [ΑΦΜ]"),
]

def guard_input(text):
    found = []
    for pattern, label in PII:
        if re.search(pattern, text):
            found.append(label)
            text = re.sub(pattern, label, text)
    return text, found

def pipeline(index, question):
    trace = []
    t = time.perf_counter()

    def step(name, cost, note):
        nonlocal t
        trace.append((name, int((time.perf_counter() - t) * 1000), cost, note))
        t = time.perf_counter()

    question, found = guard_input(question)
    step("guard εισόδου", 0.0, ", ".join(found) or "τίποτα")
    cached, kind = cache_get(question)
    step("cache", 0.0, kind or "miss")
    if cached:
        return cached, trace
    r, how, cost = route(question)
    step("router", cost, f"{r} ({how[:60]})")
    if r == "order_status":
        answer = order_status(question)
        step("κώδικας: παραγγελία", 0.0, "lookup στο orders.json")
    elif r == "documents":
        result = ask_safe(index, question)
        answer = result["answer"]
        step("RAG με παραπομπές", result["cost"], result["refused"] or f"{sum(c['ok'] for c in result['citations'])} παραπομπές ✓")
        if result["found"]:
            cache_put(question, answer)
    elif r == "complaint":
        answer = f"Λυπούμαστε. Καταγράψαμε το αίτημά σας με αριθμό T-{int(time.time()) % 100000}. Θα επικοινωνήσουμε μαζί σας σήμερα."
        step("ticket", 0.0, "δημιουργία ticket")
    elif r == "human":
        answer = "Σας συνδέω με συνάδελφο της εξυπηρέτησης. Ώρες: Δευτέρα-Παρασκευή 09:00-17:00."
        step("άνθρωπος", 0.0, "handoff")
    else:
        resp, used, errors = call_with_fallback([{"role": "system", "content": "Είσαι η Πυθία του e-shop «Μπρίκι». Απάντα ευγενικά σε μία πρόταση."}, {"role": "user", "content": question}])
        answer = resp.choices[0].message.content
        step("LLM με fallback", safe_cost(resp, used), used + (f" (απέτυχαν: {errors})" if errors else ""))
    problems = output_guard(answer)
    if problems:
        answer = "Δεν μπορώ να απαντήσω σε αυτό. Επικοινωνήστε με την εξυπηρέτηση."
    step("guard εξόδου", 0.0, ", ".join(problems) or "εντάξει")
    return answer, trace
