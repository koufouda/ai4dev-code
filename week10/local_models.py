"""Διάλεξη 20: τι έχουμε κατεβάσει στο Ollama; Μέγεθος στον δίσκο, παράμετροι, κβάντιση, δυνατότητες, άδεια.

Χρήση:  python local_models.py
"""
import sys
from pythia_models import ollama_list, ollama_show

try:
    models = ollama_list()
except OSError:
    sys.exit("Το Ollama δεν απαντά στο localhost:11434: ανοίξτε την εφαρμογή Ollama.")

print(f"{'μοντέλο':<24}{'δίσκος':>8}{'παράμ.':>9}  {'κβάντιση':<10}{'δυνατότητες':<34}άδεια")
for m in models:
    info = ollama_show(m["name"])
    details = info.get("details", {})
    caps = ", ".join(info.get("capabilities", [])) or "-"
    license_line = next((line.strip() for line in info.get("license", "").splitlines() if line.strip()), "-")
    print(f"{m['name']:<24}{m['size'] / 1e9:>6.1f}GB{details.get('parameter_size', '?'):>9}  {details.get('quantization_level', '?'):<10}{caps:<34}{license_line[:40]}")
