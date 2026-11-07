"""Διάλεξη 11: αναφορά κόστους από το costs.csv, ανά script και μοντέλο.

Κάθε κλήση των scripts της εβδομάδας γράφεται στο costs.csv. Αυτό το script τα αθροίζει.

Χρήση:  python costs_report.py
"""
import csv

totals = {}
with open("costs.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        key = (row["script"], row["model"])
        if key not in totals:
            totals[key] = [0, 0, 0, 0.0]
        totals[key][0] += 1
        totals[key][1] += int(row["input"])
        totals[key][2] += int(row["output"])
        totals[key][3] += float(row["cost"])

print(f"{'script':<15}{'μοντέλο':<30}{'κλήσεις':>8}{'είσοδος':>10}{'έξοδος':>9}{'κόστος $':>11}")
for (script, model), (calls, tokens_in, tokens_out, cost) in sorted(totals.items()):
    print(f"{script:<15}{model:<30}{calls:>8}{tokens_in:>10}{tokens_out:>9}{cost:>11.4f}")
print(f"\nΣύνολο: ${sum(t[3] for t in totals.values()):.4f}")
