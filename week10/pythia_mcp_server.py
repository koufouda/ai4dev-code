"""Διάλεξη 19: η Πυθία ως MCP server. Τα εργαλεία της διάλεξης 17, διαθέσιμα σε ΚΑΘΕ εφαρμογή που μιλά MCP
(Claude Desktop, VS Code, το δικό μας mcp_client.py).

Μόνο εργαλεία που ΔΙΑΒΑΖΟΥΝ: ελάχιστα δικαιώματα. Η ακύρωση δεν εκτίθεται εδώ.

Χρήση:  τον ξεκινά ο client (δεν τον τρέχετε μόνοι σας).
        Δοκιμή με το MCP Inspector:  mcp dev pythia_mcp_server.py
"""
import os
import sys
import contextlib
from mcp.server import MCPServer

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(sys.stderr):
    import pythia_tools

def quiet(func, *args):
    with contextlib.redirect_stdout(sys.stderr):
        return func(*args)

mcp = MCPServer("Πυθία", instructions="Εργαλεία του e-shop «Μπρίκι»: παραγγελίες, κατάλογος, έγγραφα, πράξεις. Μόνο ανάγνωση.")

@mcp.tool()
def get_order(order_id: str) -> str:
    """Κατάσταση, ημερομηνία αγοράς, προϊόντα και ποσό μιας παραγγελίας (πενταψήφιος αριθμός, π.χ. 48213)."""
    return quiet(pythia_tools.get_order, order_id)

@mcp.tool()
def get_product(code: str) -> str:
    """Τιμή, απόθεμα και περιγραφή ενός προϊόντος από τον κωδικό του (π.χ. ΜΠ-001)."""
    return quiet(pythia_tools.get_product, code)

@mcp.tool()
def find_products(text: str) -> str:
    """Έως 5 προϊόντα του καταλόγου που περιέχουν μια λέξη (π.χ. «μύλος», «espresso»)."""
    return quiet(pythia_tools.find_products, text)

@mcp.tool()
def search_docs(query: str) -> str:
    """Αναζήτηση στα έγγραφα της εταιρείας: εγχειρίδιο ΜΠ-001, εγγύηση και service, όροι πώλησης, απόρρητο."""
    return quiet(pythia_tools.search_docs, query)

@mcp.tool()
def calculate(expression: str) -> str:
    """Υπολογίζει αριθμητική έκφραση με + - * / ( ), π.χ. 3 * 10.36 * 0.9."""
    return quiet(pythia_tools.calculate, expression)

@mcp.tool()
def today() -> str:
    """Η σημερινή ημερομηνία (ΕΕΕΕ-ΜΜ-ΗΗ)."""
    return quiet(pythia_tools.today)

@mcp.resource("pythia://politiki")
def politiki() -> str:
    """Η πολιτική αποστολών, επιστροφών και ωραρίου του καταστήματος."""
    return open("katalogos.txt", encoding="utf-8").read().strip().splitlines()[-1]

@mcp.prompt()
def apantisi_pelati(email: str) -> str:
    """Πρότυπο: απάντηση σε email πελάτη με τα εργαλεία της Πυθίας."""
    return f"Είσαι η εξυπηρέτηση του e-shop «Μπρίκι». Χρησιμοποίησε τα εργαλεία για στοιχεία και γράψε σύντομη, ευγενική απάντηση σε αυτό το email:\n\n{email}"

if __name__ == "__main__":
    mcp.run()
