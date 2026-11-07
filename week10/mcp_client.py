"""Διάλεξη 19: ένας απλός MCP client. Ξεκινά τον server, ρωτά «τι εργαλεία έχεις;» και καλεί ένα.

Χρήση:  python mcp_client.py
        python mcp_client.py get_product "{\"code\": \"ΜΠ-002\"}"
"""
import sys
import os
import json
import asyncio
from mcp import Client, StdioServerParameters

tool = sys.argv[1] if len(sys.argv) > 1 else "get_order"
args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {"order_id": "48213"}

async def main():
    server = StdioServerParameters(command=sys.executable, args=["pythia_mcp_server.py"], env=dict(os.environ))
    async with Client(server) as client:
        print(f"Συνδέθηκα με: {client.server_info.name}\n")
        listing = await client.list_tools()
        for t in listing.tools:
            print(f"• {t.name}({', '.join(t.input_schema.get('properties', {}))}): {t.description}")
        print(f"\n→ {tool}({json.dumps(args, ensure_ascii=False)})")
        result = await client.call_tool(tool, args)
        print(("ΣΦΑΛΜΑ: " if result.is_error else "") + result.content[0].text)

asyncio.run(main())
