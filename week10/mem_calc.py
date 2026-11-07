"""Διάλεξη 20: πόση μνήμη θέλει ένα μοντέλο; Παράμετροι × bits ανά παράμετρο ÷ 8, συν ~20% για context και runtime.

Χρήση:  python mem_calc.py
        python mem_calc.py 8        (μόνο για 8 δισ. παραμέτρους)
"""
import sys

sizes = [float(sys.argv[1])] if len(sys.argv) > 1 else [1, 4, 8, 20, 70]
bits = [16, 8, 4]
print(f"{'παράμετροι':<12}" + "".join(f"{str(b) + ' bit':>10}  " for b in bits))
for p in sizes:
    print(f"{p:>5.0f} δισ.  " + "".join(f"{p * b / 8 * 1.2:>8.1f} GB  " for b in bits))
print("\nΟδηγός: το μοντέλο πρέπει να χωράει στη μνήμη της κάρτας γραφικών (ή στη RAM, πιο αργά), με περιθώριο για το λειτουργικό.")
