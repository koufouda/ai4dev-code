# AI for Developers: κώδικας 1ης εβδομάδας

## Προετοιμασία πριν από τη 2η διάλεξη

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

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive/OneDrive. Αντιγράψτε αυτόν τον φάκελο μέσα του ως `week01`.

Windows (PowerShell):

```powershell
cd C:\ai4dev
python -m venv .venv          # μόνο την πρώτη φορά
.venv\Scripts\activate
pip install -r week01\requirements.txt
cd week01
python check.py
```

Linux:

```bash
cd ~/ai4dev
python3 -m venv .venv         # μόνο την πρώτη φορά
source .venv/bin/activate
pip install -r week01/requirements.txt
cd week01
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

1. Python 3.13 (python.org, με «Add python.exe to PATH») και PyCharm Community (jetbrains.com/pycharm).
2. Εγκατάσταση πακέτων:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Κλειδί API της Anthropic (Claude) από το platform.claude.com, με λίγα $ σε credits και όριο δαπανών. Προαιρετικά Gemini (δωρεάν, αλλά με πολύ χαμηλό ημερήσιο όριο) ή OpenAI.
4. Αντιγράψτε το `.env.example` σε `.env` και συμπληρώστε το κλειδί σας. Το `.env` είναι ήδη στο `.gitignore`.
5. Ollama από το ollama.com και ένα τοπικό μοντέλο. Το κατεβάζετε από το σπίτι, γιατί είναι μερικά GB:

   ```bash
   ollama pull gemma3:4b      # ~3,3 GB, καλή υποστήριξη ελληνικών
   ollama pull llama3.2:1b    # ~1,3 GB, για laptop με λίγη μνήμη
   ```

### Τα αρχεία

| Αρχείο | Διάλεξη | Τι δείχνει |
|---|---|---|
| `tokens.py` | 1 | Πόσα tokens χρειάζονται τα ελληνικά σε σχέση με τα αγγλικά |
| `next_token.py` | 1 | Τις πιθανότητες για την επόμενη λέξη (χρειάζεται μοντέλο με logprobs) |
| `chatbot.py` | 1-2 | Chatbot με μνήμη. Μετά από κάθε απάντηση: tokens εισόδου/εξόδου, «σκέψη», cache, χρόνος και κόστος |
| `ask.py` | 2 | Μία κλήση με χρόνο, tokens και κόστος. Με `--local` τρέχει στο Ollama |
| `pythia.py` | 2 | Συνομιλία με μία από τρεις περσόνες: `python pythia.py 1` (Βοηθός), `2` (Πυθία, προεπιλογή), `3` (Senior dev) |
| `temperature.py` | 2 | Η ίδια ερώτηση με temperature 0 και 1 |
| `stream.py` | 2 | Streaming και χρόνος μέχρι την πρώτη λέξη |
| `arena.py` | 2 | Τυφλή σύγκριση μοντέλων με ψηφοφορία |

Τα ονόματα των μοντέλων αλλάζουν συχνά. Αν μια κλήση αποτύχει με "model not found", ελέγξτε το όνομα στη σελίδα του παρόχου και στα docs του LiteLLM (docs.litellm.ai/docs/providers).
