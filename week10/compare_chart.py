"""Διάλεξη 20: γράφημα από το results.csv. Ποιότητα (κάθετα) έναντι χρόνου απάντησης (οριζόντια), με το κόστος δίπλα.

Χρήση:  python compare_chart.py      (φτιάχνει το compare.png)
"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open("results.csv", encoding="utf-8")))
fig, ax = plt.subplots(figsize=(8, 5))
for r in rows:
    x, y = float(r["avg_seconds"]), float(r["score"]) * 100
    ax.scatter(x, y, s=120, color="#2a9d8f" if r["model"].startswith("ollama") else "#264653")
    ax.annotate(f"{r['model'].split('/')[-1]}\n${float(r['cost']):.4f}", (x, y), textcoords="offset points", xytext=(8, -4), fontsize=9)
ax.set_xlabel("Μέσος χρόνος ανά απάντηση (s)")
ax.set_ylabel("Σωστά (%)")
ax.set_ylim(0, 105)
ax.set_title("Ποιότητα έναντι ταχύτητας (πάνω αριστερά = καλύτερα)")
ax.grid(alpha=0.3)
fig.savefig("compare.png", dpi=150, bbox_inches="tight")
print("Το γράφημα στο compare.png")
