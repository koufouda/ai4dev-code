"""Διάλεξη 21: «καπνός;» Μετά από κάθε εγκατάσταση: απαντά η εφαρμογή; Ένα /health και μία ερώτηση.

Χρήση:  python smoke_test.py                        (http://localhost:8000)
        python smoke_test.py https://pythia.example.com
"""
import sys
import json
import time
import urllib.request

url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
health = json.load(urllib.request.urlopen(url + "/health", timeout=10))
print("health:", health)
body = json.dumps({"question": "Πόσο κοστίζει η ΜΠ-001;"}).encode()
req = urllib.request.Request(url + "/chat", data=body, headers={"Content-Type": "application/json"})
start = time.perf_counter()
answer = json.load(urllib.request.urlopen(req, timeout=120))
print(f"chat ({time.perf_counter() - start:.1f}s):", answer["answer"], "\n", answer["disclosure"])
sys.exit(0 if health["status"] == "ok" and "349" in answer["answer"] else 1)
