# Εβδομάδα 12 · Η Πυθία στο internet

Κώδικας για τη διάλεξη 23 (ολοκλήρωση και εγκατάσταση). Η διάλεξη 24 είναι οι παρουσιάσεις.

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

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive/OneDrive. Αντιγράψτε αυτόν τον φάκελο μέσα του ως `week12`.

Windows (PowerShell):

```powershell
cd C:\ai4dev
python -m venv .venv          # μόνο την πρώτη φορά
.venv\Scripts\activate
pip install -r week12\requirements.txt
cd week12
python check.py
```

Linux:

```bash
cd ~/ai4dev
python3 -m venv .venv         # μόνο την πρώτη φορά
source .venv/bin/activate
pip install -r week12/requirements.txt
cd week12
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

Ίδιος κώδικας με την εβδομάδα 11, με τρεις προσθήκες στο `app.py`:
- `APP_TOKEN`: αν οριστεί, το `/chat` θέλει την κεφαλίδα `X-Token` (μια δημόσια διεύθυνση = ο καθένας ξοδεύει τα λεφτά σας).
- `LOG_STDOUT=1`: τα logs πάνε και στο stdout, για να τα κρατά η υπηρεσία cloud.
- Ένα test ακόμα (11 συνολικά) για το `APP_TOKEN`.

| Αρχείο | Τι κάνει |
|---|---|
| DEPLOY.md | Τρεις δρόμοι: Azure Container Apps, Google Cloud Run, Render · embeddings χωρίς Ollama · κλειδιά ως secrets · σβήσιμο |
| remote_eval.py | Το σύνολο δοκιμών πάνω στην εγκατεστημένη εφαρμογή: σωστά, p50/p95, σφάλματα |
| release_check.py | secret_scan → pytest → smoke → remote_eval: «ΈΤΟΙΜΟ για τη διάλεξη 24» |
| smoke_test.py, traffic.py | Στέλνουν πλέον και το `X-Token` (από `$env:APP_TOKEN`) |

Οι υπόλοιποι φάκελοι και αρχεία είναι της εβδομάδας 11 (Dockerfile, compose, CI, tests, dashboard, privacy).

**Μετά τη διάλεξη 24: σβήστε ό,τι φτιάξατε στο cloud.**
