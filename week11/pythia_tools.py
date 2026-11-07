"""Εβδομάδα 9, διάλεξη 17: η Πυθία με εργαλεία. Συναρτήσεις που καλεί το μοντέλο, τα σχήματά τους, και ο βρόχος.

Χτίζει πάνω στο pythia_rag.py (εβδομάδα 7) και στο pythia_safe.py (διάλεξη 15).
"""
import json
import ast
import operator
import datetime
from pythia_rag import MODEL, completion, safe_cost, normalize, load_index, search

def get_order(order_id):
    orders = json.load(open("orders.json", encoding="utf-8"))
    if order_id not in orders:
        return f"Δεν υπάρχει παραγγελία με αριθμό {order_id}."
    return json.dumps({"order_id": order_id, **orders[order_id]}, ensure_ascii=False)

def cancel_order(order_id):
    orders = json.load(open("orders.json", encoding="utf-8"))
    if order_id not in orders:
        return f"Δεν υπάρχει παραγγελία με αριθμό {order_id}."
    if orders[order_id]["status"] != "σε προετοιμασία":
        return f"Η παραγγελία {order_id} δεν ακυρώνεται γιατί είναι «{orders[order_id]['status']}». Ο πελάτης μπορεί να κάνει επιστροφή μέσα σε 14 ημέρες."
    with open("actions.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  ακύρωση {order_id}\n")
    return f"Η παραγγελία {order_id} ακυρώθηκε. Επιστροφή {orders[order_id]['total']:.2f} € σε 5-7 εργάσιμες."

def get_product(code):
    code = code.strip().upper().replace("MP", "ΜΠ")
    for line in open("katalogos.txt", encoding="utf-8"):
        if line.startswith(code + " |"):
            return line.strip()
    return f"Δεν υπάρχει προϊόν με κωδικό {code}."

def find_products(text):
    t = normalize(text)
    found = [line.strip() for line in open("katalogos.txt", encoding="utf-8") if line.startswith("ΜΠ-") and t in normalize(line)]
    if not found:
        return f"Κανένα προϊόν με «{text}»."
    return "\n".join(found[:5]) + (f"\n… και άλλα {len(found) - 5}. Δοκίμασε πιο συγκεκριμένη λέξη." if len(found) > 5 else "")

_index = None

def search_docs(query):
    global _index
    if _index is None:
        _index = load_index()
    results = search(_index, query, "hybrid", 3)
    return "\n\n".join(f"[{c['source']} ({c['place']})]\n{c['text']}" for _, c in results)

OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.USub: operator.neg}

def calculate(expression):
    def value(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](value(node.left), value(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](value(node.operand))
        raise ValueError("επιτρέπονται μόνο αριθμοί και + - * / ( )")
    tree = ast.parse(expression.replace(",", "."), mode="eval")
    return str(round(value(tree.body), 2))

def today():
    return datetime.date.today().isoformat()

TOOLS = [
    {"type": "function", "function": {
        "name": "get_order",
        "description": "Κατάσταση, ημερομηνία αγοράς, προϊόντα και ποσό μιας παραγγελίας. Χρησιμοποίησέ το όταν ο πελάτης δίνει αριθμό παραγγελίας.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string", "description": "Πενταψήφιος αριθμός παραγγελίας, π.χ. 48213"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {
        "name": "cancel_order",
        "description": "ΑΚΥΡΩΝΕΙ μια παραγγελία. Μόνο όταν ο πελάτης το ζητά ρητά («ακύρωσε»), όχι όταν απλώς ρωτά αν γίνεται.",
        "parameters": {"type": "object", "properties": {"order_id": {"type": "string", "description": "Πενταψήφιος αριθμός παραγγελίας"}}, "required": ["order_id"]}}},
    {"type": "function", "function": {
        "name": "get_product",
        "description": "Τιμή, απόθεμα και περιγραφή ενός προϊόντος από τον κωδικό του.",
        "parameters": {"type": "object", "properties": {"code": {"type": "string", "description": "Κωδικός προϊόντος, π.χ. ΜΠ-001"}}, "required": ["code"]}}},
    {"type": "function", "function": {
        "name": "find_products",
        "description": "Αναζήτηση προϊόντων στον κατάλογο με μια λέξη (π.χ. «μύλος», «espresso»). Επιστρέφει έως 5 με κωδικό, τιμή και απόθεμα.",
        "parameters": {"type": "object", "properties": {"text": {"type": "string", "description": "Μία λέξη από το όνομα ή την περιγραφή"}}, "required": ["text"]}}},
    {"type": "function", "function": {
        "name": "search_docs",
        "description": "Αναζήτηση στα έγγραφα της εταιρείας: εγχειρίδιο ΜΠ-001 (κωδικοί σφάλματος, συντήρηση), εγγύηση και service, όροι πώλησης, απόρρητο.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "Τι ψάχνουμε, με λέξεις-κλειδιά"}}, "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "calculate",
        "description": "Υπολογίζει αριθμητική έκφραση με + - * / ( ). Χρησιμοποίησέ το για ΚΑΘΕ πράξη με τιμές ή ποσοστά.",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string", "description": "π.χ. 3 * 10.36 * 0.9"}}, "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "today",
        "description": "Η σημερινή ημερομηνία (ΕΕΕΕ-ΜΜ-ΗΗ). Χρειάζεται για προθεσμίες και εγγυήσεις.",
        "parameters": {"type": "object", "properties": {}, "required": []}}},
]

FUNCTIONS = {"get_order": get_order, "cancel_order": cancel_order, "get_product": get_product, "find_products": find_products,
             "search_docs": search_docs, "calculate": calculate, "today": today}

def run_tool(name, arguments):
    try:
        args = json.loads(arguments or "{}")
    except json.JSONDecodeError:
        return "Σφάλμα: τα ορίσματα δεν είναι έγκυρο JSON."
    if name not in FUNCTIONS:
        return f"Σφάλμα: δεν υπάρχει εργαλείο {name}."
    try:
        return str(FUNCTIONS[name](**args))
    except Exception as e:
        return f"Σφάλμα: {type(e).__name__}: {e}"

SYSTEM = ("Είσαι η Πυθία, βοηθός του e-shop «Μπρίκι». Για τιμές, απόθεμα, παραγγελίες, ημερομηνίες και πράξεις ΧΡΗΣΙΜΟΠΟΙΕΙΣ τα εργαλεία· "
          "δεν μαντεύεις αριθμούς και δεν κάνεις πράξεις με το μυαλό. Ακυρώνεις παραγγελία μόνο αν ο πελάτης το ζητά ρητά. "
          "Αν κάτι δεν γίνεται με τα εργαλεία που έχεις, το λες. Απαντάς στα ελληνικά, σε 1-3 προτάσεις.")

def chat_with_tools(question, tools=TOOLS, max_rounds=4, model=MODEL):
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    trace = []
    cost = 0.0
    for _ in range(max_rounds):
        resp = completion(model=model, messages=messages, tools=tools, num_retries=3)
        cost += safe_cost(resp, model)
        msg = resp.choices[0].message
        if not msg.tool_calls:
            return msg.content, trace, cost
        messages.append(msg)
        for call in msg.tool_calls:
            result = run_tool(call.function.name, call.function.arguments)
            trace.append((call.function.name, call.function.arguments, result))
            messages.append({"role": "tool", "tool_call_id": call.id, "name": call.function.name, "content": result})
    return "Δεν κατάφερα να ολοκληρώσω. Επικοινωνήστε με την εξυπηρέτηση.", trace, cost

def print_trace(trace):
    for name, args, result in trace:
        print(f"   → {name}({args})  =  {' '.join(result.split())[:90]}")

def contains_all(answer, expected):
    a = normalize(answer or "")
    return all(any(normalize(alt) in a for alt in e.split("|")) for e in expected)

if __name__ == "__main__":
    assert calculate("3 * 10,36 * (1 - 0.1)") == "27.97"
    assert run_tool("calculate", '{"expression": "__import__(\'os\')"}').startswith("Σφάλμα")
    assert run_tool("delete_all", "{}").startswith("Σφάλμα")
    assert contains_all("Κοστίζει 27,97 €", ["27.97|27,97"])
    print("OK")
