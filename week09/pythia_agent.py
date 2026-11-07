"""Εβδομάδα 9, διάλεξη 18: ο agent. Ο βρόχος σκέψη → ενέργεια → παρατήρηση, με όρια.

Χτίζει πάνω στο pythia_tools.py (διάλεξη 17).
"""
import re
import time
from pythia_rag import MODEL, completion, safe_cost
from pythia_tools import TOOLS, SYSTEM, run_tool, get_order, get_product, search_docs

AGENT_SYSTEM = SYSTEM + (" Λύνεις το πρόβλημα βήμα-βήμα. Πριν από κάθε εργαλείο γράφεις ΜΙΑ σύντομη πρόταση με το τι θέλεις να μάθεις και γιατί. "
                         "Όταν έχεις αρκετά στοιχεία, δίνεις την τελική απάντηση χωρίς εργαλείο.")

def agent(task, tools=TOOLS, max_steps=8, max_cost=0.05, model=MODEL, verbose=True):
    messages = [{"role": "system", "content": AGENT_SYSTEM}, {"role": "user", "content": task}]
    steps = []
    seen = set()
    cost, start = 0.0, time.perf_counter()
    for step in range(1, max_steps + 1):
        resp = completion(model=model, messages=messages, tools=tools, num_retries=3)
        cost += safe_cost(resp, model)
        msg = resp.choices[0].message
        if not msg.tool_calls:
            if verbose:
                print(f"[{step}] Απάντηση: {msg.content}")
            return {"answer": msg.content, "steps": steps, "cost": cost, "seconds": time.perf_counter() - start, "stopped": "απάντησε"}
        if verbose and msg.content:
            print(f"[{step}] Σκέψη: {re.sub(r'^Σκέψη:\s*', '', ' '.join(msg.content.split()))}")
        messages.append(msg)
        for call in msg.tool_calls:
            key = (call.function.name, call.function.arguments)
            if key in seen:
                result = "Σφάλμα: έχεις ήδη κάνει αυτή την κλήση με τα ίδια ορίσματα. Δοκίμασε κάτι άλλο ή απάντησε με όσα ξέρεις."
            else:
                result = run_tool(call.function.name, call.function.arguments)
            seen.add(key)
            steps.append((step, call.function.name, call.function.arguments, result))
            messages.append({"role": "tool", "tool_call_id": call.id, "name": call.function.name, "content": result})
            if verbose:
                print(f"    Ενέργεια: {call.function.name}({call.function.arguments})\n    Παρατήρηση: {' '.join(result.split())[:110]}")
        if cost > max_cost:
            return {"answer": "Σταμάτησα: ξεπεράστηκε το όριο κόστους. Το αίτημα πάει σε άνθρωπο.", "steps": steps, "cost": cost, "seconds": time.perf_counter() - start, "stopped": "όριο κόστους"}
    return {"answer": "Σταμάτησα: πάρα πολλά βήματα. Το αίτημα πάει σε άνθρωπο.", "steps": steps, "cost": cost, "seconds": time.perf_counter() - start, "stopped": "όριο βημάτων"}

def fixed_workflow(task, model=MODEL):
    start = time.perf_counter()
    facts = []
    for order_id in re.findall(r"\b\d{5}\b", task):
        facts.append(get_order(order_id))
    for code in re.findall(r"ΜΠ-\d{3}", task):
        facts.append(get_product(code))
    facts.append(search_docs(task))
    user = "<facts>\n" + "\n\n".join(facts) + "\n</facts>\n\n<question>" + task + "</question>"
    resp = completion(model=model, messages=[{"role": "system", "content": SYSTEM + " Απαντάς μόνο από τα <facts>."}, {"role": "user", "content": user}], num_retries=3)
    return {"answer": resp.choices[0].message.content, "steps": [], "cost": safe_cost(resp, model), "seconds": time.perf_counter() - start, "stopped": "workflow"}
