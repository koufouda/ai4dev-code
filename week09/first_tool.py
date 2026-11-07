"""Διάλεξη 17: το πρώτο εργαλείο, βήμα-βήμα. Τι στέλνουμε, τι ζητά το μοντέλο, τι του επιστρέφουμε.

Χρήση:  python first_tool.py
        python first_tool.py "Έχετε σε απόθεμα τη ΜΠ-002;"
"""
import sys
import json
from pythia_rag import MODEL, completion, safe_cost
from pythia_tools import TOOLS, run_tool

question = sys.argv[1] if len(sys.argv) > 1 else "Πόσο κοστίζει η ΜΠ-001;"
tools = [t for t in TOOLS if t["function"]["name"] == "get_product"]
messages = [{"role": "system", "content": "Είσαι η Πυθία του e-shop «Μπρίκι». Για τιμές χρησιμοποίησε το εργαλείο. Απάντα σε 1-2 προτάσεις."},
            {"role": "user", "content": question}]

print("=== 1. Στέλνουμε την ερώτηση και το σχήμα του εργαλείου ===")
print(json.dumps(tools[0], ensure_ascii=False, indent=1))

resp = completion(model=MODEL, messages=messages, tools=tools, num_retries=3)
msg = resp.choices[0].message
print("\n=== 2. Το μοντέλο ΔΕΝ απαντά. Ζητά να τρέξουμε εργαλείο ===")
if msg.tool_calls:
    call = msg.tool_calls[0]
    print(f"κείμενο: {msg.content!r}\nεργαλείο: {call.function.name}\nορίσματα: {call.function.arguments}\nid: {call.id}")
else:
    print("Απάντησε χωρίς εργαλείο:", msg.content)
    sys.exit()

print("\n=== 3. ΕΜΕΙΣ τρέχουμε τη συνάρτηση Python ===")
result = run_tool(call.function.name, call.function.arguments)
print(result)

print("\n=== 4. Στέλνουμε το αποτέλεσμα πίσω, και το μοντέλο απαντά ===")
messages.append(msg)
messages.append({"role": "tool", "tool_call_id": call.id, "name": call.function.name, "content": result})
resp2 = completion(model=MODEL, messages=messages, tools=tools, num_retries=3)
print(f"Πυθία: {resp2.choices[0].message.content}\n\n2 κλήσεις | ${safe_cost(resp, MODEL) + safe_cost(resp2, MODEL):.5f}")
