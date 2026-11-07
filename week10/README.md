# Εβδομάδα 10 · MCP, ασφάλεια agents, ανοικτά μοντέλα

Κώδικας για τις διαλέξεις 19 (MCP, frameworks, ασφάλεια agents) και 20 (ανοικτά μοντέλα και σύγκριση με μετρήσεις).

Για κάθε αρχείο `.py` υπάρχει ένα `.txt` με το ίδιο όνομα: τι κάνει και πώς το τρέχετε.

## 1. Εργαλεία

Αναλυτικές οδηγίες για Windows 11 και Linux: [INSTALL.md](../INSTALL.md) στο repository του μαθήματος. Σύντομα:

| Εργαλείο | Windows 11 (PowerShell) | Linux (Ubuntu/Debian) |
|---|---|---|
| Python 3.13 (Linux: 3.11+) | `winget install -e --id Python.Python.3.13` | `sudo apt install python3 python3-venv python3-pip` |
| VS Code + Python extension | `winget install -e --id Microsoft.VisualStudioCode` | `sudo snap install code --classic` |
| Ollama | `winget install -e --id Ollama.Ollama` | `curl -fsSL https://ollama.com/install.sh \| sh` |

Τοπικά μοντέλα που χρειάζεται αυτή η εβδομάδα (μία φορά):

```
ollama pull gemma3:4b
ollama pull llama3.2:1b
ollama pull embeddinggemma
ollama pull qwen3.5:4b
ollama pull gemma4:e2b
```

Στα Windows, αν το `python` ανοίγει το Microsoft Store: Ρυθμίσεις → Εφαρμογές → Ρυθμίσεις για προχωρημένους → Ψευδώνυμα εκτέλεσης εφαρμογών, και κλείστε τα python.exe / python3.exe.

## 2. Στήσιμο (μία φορά)

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive/OneDrive. Αντιγράψτε αυτόν τον φάκελο μέσα του ως `week10`.

Windows (PowerShell):

```powershell
cd C:\ai4dev
python -m venv .venv          # μόνο την πρώτη φορά
.venv\Scripts\activate
pip install -r week10\requirements.txt
cd week10
python check.py
```

Linux:

```bash
cd ~/ai4dev
python3 -m venv .venv         # μόνο την πρώτη φορά
source .venv/bin/activate
pip install -r week10/requirements.txt
cd week10
python check.py
```

Αν το `activate` στα Windows βγάλει σφάλμα για «execution policy»: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

Στο VS Code: File → Open Folder → `C:\ai4dev` (ή `~/ai4dev`), μετά Ctrl+Shift+P → `>Python: Select Interpreter` → αυτόν με το `.venv`.

## 3. Κλειδιά API (.env)

1. Κλειδί Anthropic: platform.claude.com → Settings → API keys → Create key. Χρειάζεται υπόλοιπο σε credits (Billing). Βάλτε και όριο δαπάνης.
2. Αντιγράψτε το `.env.example` ως `.env` στον **γονικό** φάκελο (`C:\ai4dev\.env` ή `~/ai4dev/.env`). Τα scripts κάθε εβδομάδας το βρίσκουν εκεί.
   - Windows: `copy .env.example ..\.env` και μετά `notepad ..\.env`
   - Linux: `cp .env.example ../.env` και μετά `nano ../.env`
3. Γράψτε το κλειδί μετά το `ANTHROPIC_API_KEY=`, χωρίς κενά και χωρίς εισαγωγικά. Τα υπόλοιπα κλειδιά (OpenAI, Gemini) είναι προαιρετικά.
4. Τρέξτε `python check.py`: δείχνει αν βρήκε κλειδί, ποτέ την τιμή του.

Αν έχετε ήδη `.env` από προηγούμενη εβδομάδα, συγκρίνετε με το `.env.example` και προσθέστε μόνο τις νέες γραμμές.

**Το `.env` δεν μπαίνει ποτέ σε Drive, email, chat ή GitHub, και δεν φαίνεται ποτέ στην οθόνη.** Αν διαρρεύσει, ακυρώστε το κλειδί αμέσως από την κονσόλα.

## 4. Τα αρχεία της εβδομάδας

### Διάλεξη 19

| Αρχείο | Τι κάνει |
|---|---|
| pythia_mcp_server.py | Η Πυθία ως MCP server (μόνο εργαλεία ανάγνωσης, ένα resource, ένα prompt) |
| mcp_client.py | Απλός MCP client: λίστα εργαλείων και μία κλήση |
| mcp_agent.py | Ο agent της διάλεξης 18 με εργαλεία από τον MCP server |
| claude_desktop_config.json | Ρύθμιση για να δει το Claude Desktop την Πυθία |
| pythia_guard.py | Φύλακας: έγκριση από άνθρωπο για ενέργειες μετά από μη έμπιστο κείμενο (Rule of Two) |
| injection_agent.py | Ο agent διαβάζει email με κρυφή εντολή (`--guard`, `--auto`, `--readonly`) |
| inbox.json | Τρία email πελατών, το ένα με prompt injection |

### Διάλεξη 20

| Αρχείο | Τι κάνει |
|---|---|
| pythia_models.py | Κοινές συναρτήσεις: λίστα μοντέλων, κλήση με χρόνο και κόστος, Ollama API |
| local_models.py | Τα τοπικά μοντέλα: μέγεθος, κβάντιση, δυνατότητες, άδεια |
| mem_calc.py | Πόση μνήμη θέλει ένα μοντέλο |
| speed_test.py | Χρόνος μέχρι την 1η λέξη και tokens/s |
| compare_models.py | 16 δοκιμές (model_cases.json) σε όλα τα μοντέλα του models.txt → results.csv |
| compare_chart.py | Γράφημα ποιότητας έναντι χρόνου → compare.png |
| local_agent.py | Ο agent με τοπικό μοντέλο (`--model`) |

Το `cancel_order` γράφει μόνο στο `actions.log` (δεν αλλάζει το orders.json).
Όλες οι εντολές με τη σειρά των διαφανειών: `questions.txt`.
