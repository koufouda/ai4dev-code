# Εβδομάδα 11 · Η Πυθία βγαίνει από το laptop

Κώδικας για τις διαλέξεις 21 (Docker, κλειδιά, CI) και 22 (logs, παρακολούθηση, GDPR, AI Act).

Για κάθε αρχείο `.py` υπάρχει ένα `.txt` με το ίδιο όνομα: τι κάνει και πώς το τρέχετε.

## 1. Εργαλεία

Αναλυτικές οδηγίες για Windows 11 και Linux: [INSTALL.md](../INSTALL.md) στο repository του μαθήματος. Σύντομα:

| Εργαλείο | Windows 11 (PowerShell) | Linux (Ubuntu/Debian) |
|---|---|---|
| Python 3.13 (Linux: 3.11+) | `winget install -e --id Python.Python.3.13` | `sudo apt install python3 python3-venv python3-pip` |
| VS Code + Python extension | `winget install -e --id Microsoft.VisualStudioCode` | `sudo snap install code --classic` |
| Ollama | `winget install -e --id Ollama.Ollama` | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Git | `winget install -e --id Git.Git` | `sudo apt install git` |
| Docker | `wsl --install` και `winget install -e --id Docker.DockerDesktop` | `curl -fsSL https://get.docker.com \| sh` |

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

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive/OneDrive. Αντιγράψτε αυτόν τον φάκελο μέσα του ως `week11`.

Windows (PowerShell):

```powershell
cd C:\ai4dev
python -m venv .venv          # μόνο την πρώτη φορά
.venv\Scripts\activate
pip install -r week11\requirements.txt
cd week11
python check.py
```

Linux:

```bash
cd ~/ai4dev
python3 -m venv .venv         # μόνο την πρώτη φορά
source .venv/bin/activate
pip install -r week11/requirements.txt
cd week11
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

### Η εφαρμογή

`app.py`: το API με εργαλεία (διάλεξη 17) έτοιμο για παραγωγή: `/health`, `/chat` (με δήλωση AI,
απόκρυψη προσωπικών, ψευδώνυμο χρήστη, log σε `logs/ΕΕΕΕ-ΜΜ-ΗΗ.jsonl`), `/feedback`.

### Διάλεξη 21

| Αρχείο | Τι κάνει |
|---|---|
| Dockerfile, .dockerignore | Η εικόνα της Πυθίας (χωρίς .env, όχι root, με healthcheck) |
| docker-compose.yml | Θύρα, κλειδιά από `..\.env`, Ollama του υπολογιστή, logs σε volume |
| smoke_test.py | /health και μία ερώτηση στην εφαρμογή που τρέχει |
| secret_scan.py | Κλειδιά στον κώδικα; Είναι το .env στα .gitignore/.dockerignore; |
| tests/test_pythia.py, pytest.ini | 10 tests χωρίς κλειδί (με «ψεύτικο» μοντέλο) |
| ci_eval.py | Το eval εργαλείων ως πύλη (exit code 1 αν αποτύχει) |
| .github/workflows/ci.yml | GitHub Actions: secret_scan, tests, docker build, eval με το κουμπί |

### Διάλεξη 22

| Αρχείο | Τι κάνει |
|---|---|
| traffic.py | Ερωτήσεις «πελατών» και feedback, για να γεμίσουν τα logs (`--url` για το container) |
| dashboard.py | Όγκος, σφάλματα, p95, κόστος, εργαλεία, προσωπικά που κρύφτηκαν, feedback, ειδοποιήσεις |
| privacy.py | GDPR: `--export`, `--erase`, `--retention` |

Το repository για το GitHub είναι ο φάκελος week11 (με το `.github`). Το `.env` ΔΕΝ μπαίνει ποτέ.
Όλες οι εντολές με τη σειρά των διαφανειών: `questions.txt`.
