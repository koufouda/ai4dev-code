# Εβδομάδα 5 · Η Πυθία μιλά JSON και μετριέται

Κώδικας για τις διαλέξεις 9 (prompting, structured outputs, FastAPI) και 10 (δοκιμές και αξιολόγηση).

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
```

Στα Windows, αν το `python` ανοίγει το Microsoft Store: Ρυθμίσεις → Εφαρμογές → Ρυθμίσεις για προχωρημένους → Ψευδώνυμα εκτέλεσης εφαρμογών, και κλείστε τα python.exe / python3.exe.

## 2. Στήσιμο (μία φορά)

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive/OneDrive. Αντιγράψτε αυτόν τον φάκελο μέσα του ως `week05`.

Windows (PowerShell):

```powershell
cd C:\ai4dev
python -m venv .venv          # μόνο την πρώτη φορά
.venv\Scripts\activate
pip install -r week05\requirements.txt
cd week05
python check.py
```

Linux:

```bash
cd ~/ai4dev
python3 -m venv .venv         # μόνο την πρώτη φορά
source .venv/bin/activate
pip install -r week05/requirements.txt
cd week05
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

### Τα αρχεία

| Αρχείο | Τι κάνει | Διάλεξη |
|---|---|---|
| pythia_ticket.py | Το σχήμα Ticket, τα prompts v1/v2 και η extract_ticket | 9, 10 |
| prompt_vs.py | Κακό και καλό prompt στο ίδιο email | 9 |
| few_shot.py | Κατάταξη με και χωρίς παραδείγματα | 9 |
| json_please.py | JSON χωρίς σχήμα, τρεις φορές | 9 |
| ticket.py | Ένα email γίνεται ticket | 9 |
| app.py | Το ticket ως API (`uvicorn app:app --reload`, μετά http://127.0.0.1:8000/docs) | 9 |
| inbox.py | Όλα τα email σε ουρά κατά προτεραιότητα | 9 |
| eval_cases.json | Οι 10 δοκιμές με τις σωστές απαντήσεις | 10 |
| run_eval.py | Σκορ στις δοκιμές (`--prompt`, `--model`, `--repeat`) | 10 |
| judge.py | Ένα μοντέλο βαθμολογεί τις περιλήψεις | 10 |
| test_tickets.py | Οι δοκιμές ως pytest (`pytest -v test_tickets.py`) | 10 |
| check.py | Έλεγχος περιβάλλοντος | όλες |
| questions.txt | Όλες οι εντολές με τη σειρά των διαφανειών | όλες |

Τα email στο `samples/` είναι φανταστικά, για το φανταστικό e-shop «Μπρίκι». Το `08_injection.txt` περιέχει σκόπιμα
μια «εντολή» μέσα στο email, για να δούμε αν η Πυθία την αγνοεί.

### Κόστος

Ένα πλήρες `run_eval.py` είναι 10 κλήσεις. Το `judge.py` είναι 20. Με το Claude Haiku κοστίζουν λίγα σεντ.
Με `--model ollama_chat/gemma3:4b` (ή ό,τι έχετε στο MODEL_LOCAL) το κόστος είναι 0.

### Ασφάλεια

Το `.env` με τα κλειδιά δεν μπαίνει ποτέ σε zip, git ή κοινόχρηστο φάκελο.
