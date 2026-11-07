# Εβδομάδα 8 · RAG που αξίζει εμπιστοσύνη και μοτίβα αρχιτεκτονικής

Κώδικας για τις διαλέξεις 15 (παραπομπές, «δεν ξέρω», prompt injection, αξιολόγηση) και 16 (router, fallback, cache, guardrails).

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
```

Στα Windows, αν το `python` ανοίγει το Microsoft Store: Ρυθμίσεις → Εφαρμογές → Ρυθμίσεις για προχωρημένους → Ψευδώνυμα εκτέλεσης εφαρμογών, και κλείστε τα python.exe / python3.exe.

## 2. Στήσιμο (μία φορά)

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive/OneDrive. Αντιγράψτε αυτόν τον φάκελο μέσα του ως `week08`.

Windows (PowerShell):

```powershell
cd C:\ai4dev
python -m venv .venv          # μόνο την πρώτη φορά
.venv\Scripts\activate
pip install -r week08\requirements.txt
cd week08
python check.py
```

Linux:

```bash
cd ~/ai4dev
python3 -m venv .venv         # μόνο την πρώτη φορά
source .venv/bin/activate
pip install -r week08/requirements.txt
cd week08
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

### Δεδομένα

| Αρχείο | Τι είναι |
|---|---|
| docs/ | Τα 4 έγγραφα του «Μπρίκι» (ίδια με την εβδομάδα 7) |
| docs_attack/Fthinoporini_Prosfora.pdf | PDF με κρυφό λευκό κείμενο (prompt injection) για το demo. Δεν μπαίνει ποτέ στη βάση db/. Το email και ο κωδικός μέσα του είναι φανταστικά. |
| rag_cases.json | 20 ερωτήσεις με απάντηση |
| unanswerable.json | 6 ερωτήσεις που τα έγγραφα δεν απαντούν |
| orders.json | 5 φανταστικές παραγγελίες |

### Διάλεξη 15

| Αρχείο | Τι κάνει |
|---|---|
| pythia_safe.py | Παραπομπές που ελέγχονται, κατώφλι «δεν ξέρω», σάρωση εγγράφων, έλεγχος εξόδου, `ask_safe` |
| cite.py | Απάντηση με παραπομπές ✓/✗ (`--show`) |
| idk_demo.py | Ερωτήσεις χωρίς απάντηση, πριν και μετά (`--threshold`) |
| scan_docs.py | Σάρωση εγγράφων για κρυφές εντολές |
| attack_demo.py | Το «μολυσμένο» PDF, χωρίς και με άμυνες |
| eval_answers.py | Σωστές, «δεν ξέρω», παραπομπές, πιστότητα (`--threshold`, `--judge`) |
| app_safe.py | API με άμυνες: `uvicorn app_safe:app --reload` |

### Διάλεξη 16

| Αρχείο | Τι κάνει |
|---|---|
| pythia_arch.py | Router, order_status, fallback, cache, guard εισόδου, pipeline |
| router_demo.py | Πού πηγαίνει κάθε μήνυμα |
| fallback_demo.py | Τι γίνεται όταν πέφτει ο πάροχος |
| answer_cache.py | Cache απαντήσεων: exact και semantic |
| guard_demo.py | Προσωπικά δεδομένα πριν και μετά |
| pipeline_demo.py | Όλα μαζί, με χρόνο και κόστος ανά βήμα |

Όλες οι εντολές με τη σειρά των διαφανειών: `questions.txt`.

Το `.env` με τα κλειδιά μένει στο `C:\ai4dev`. Ποτέ στο Drive, στο zip ή στην οθόνη.
