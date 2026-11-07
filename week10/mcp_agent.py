"""Διάλεξη 19: ο agent της διάλεξης 18 με εργαλεία από MCP server. Ο agent δεν ξέρει από πριν ποια εργαλεία υπάρχουν:
τα ανακαλύπτει από τον server. Αλλάζεις server, αλλάζουν τα εργαλεία, ο κώδικας του agent μένει ίδιος.

Χρήση:  python mcp_agent.py
        python mcp_agent.py "Η παραγγελία 48213: τι προϊόν είναι και πόσο κάνουν άλλα δύο;"
"""
import sys
import os
import json
import asyncio
from mcp import Client, StdioServerParameters
from pythia_rag import MODEL, completion, safe_cost
from pythia_agent import AGENT_SYSTEM

task = sys.argv[1] if len(sys.argv) > 1 else "Η παραγγελία 41188 έχει μια ΜΠ-001 που γράφει E05. Καλύπτεται από την εγγύηση;"

def to_litellm(t):
    return {"type": "function", "function": {"name": t.name, "description": t.description, "parameters": t.input_schema}}

async def main(max_steps=8):
    async with Client(StdioServerParameters(command=sys.executable, args=["pythia_mcp_server.py"], env=dict(os.environ))) as client:
        tools = [to_litellm(t) for t in (await client.list_tools()).tools]
        print(f"Εργαλεία από τον server: {[t['function']['name'] for t in tools]}\n### {task}")
        messages = [{"role": "system", "content": AGENT_SYSTEM}, {"role": "user", "content": task}]
        cost = 0.0
        for step in range(1, max_steps + 1):
            resp = completion(model=MODEL, messages=messages, tools=tools, num_retries=3)
            cost += safe_cost(resp, MODEL)
            msg = resp.choices[0].message
            if not msg.tool_calls:
                print(f"[{step}] Απάντηση: {msg.content}\n   [${cost:.5f}]")
                return
            messages.append(msg)
            for call in msg.tool_calls:
                result = await client.call_tool(call.function.name, json.loads(call.function.arguments or "{}"))
                text = result.content[0].text if result.content else ""
                print(f"    Ενέργεια (MCP): {call.function.name}({call.function.arguments})\n    Παρατήρηση: {' '.join(text.split())[:110]}")
                messages.append({"role": "tool", "tool_call_id": call.id, "name": call.function.name, "content": text})
        print("Σταμάτησα: πάρα πολλά βήματα.")

asyncio.run(main())
