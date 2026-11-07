"""Διάλεξη 20: ο agent της διάλεξης 18 με τοπικό μοντέλο. Τα ίδια εργαλεία, χωρίς να φύγει τίποτα από τον υπολογιστή.

Χρήση:  python local_agent.py
        python local_agent.py --model ollama_chat/gemma4:e2b
        python local_agent.py --model anthropic/claude-haiku-5-5 "Πόσο κάνουν 3 ΜΠ-004 με έκπτωση 10%;"
"""
import sys
from pythia_agent import agent
from pythia_rag import option

model = option(sys.argv, "--model", "ollama_chat/qwen3.5:4b")
rest = [a for a in sys.argv[1:] if a != "--model" and a != model]
task = rest[0] if rest else "Η παραγγελία 48213: τι προϊόν είναι και πόσο θα κόστιζαν άλλα δύο ίδια;"
print(f"### {model}\n### {task}")
r = agent(task, model=model)
print(f"\n   [{len(r['steps'])} ενέργειες | {r['seconds']:.1f}s | σταμάτησε: {r['stopped']}]")
