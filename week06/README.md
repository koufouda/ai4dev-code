# Εβδομάδα 6 · Μνήμη και νόημα

Κώδικας για τις διαλέξεις 11 (ιστορικό συνομιλίας, context, prompt caching, κόστος) και 12 (embeddings, vector database, αναζήτηση με νόημα).

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

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive/OneDrive. Αντιγράψτε αυτόν τον φάκελο μέσα του ως `week06`.

Windows (PowerShell):

```powershell
cd C:\ai4dev
python -m venv .venv          # μόνο την πρώτη φορά
.venv\Scripts\activate
pip install -r week06\requirements.txt
cd week06
python check.py
```

Linux:

```bash
cd ~/ai4dev
python3 -m venv .venv         # μόνο την πρώτη φορά
source .venv/bin/activate
pip install -r week06/requirements.txt
cd week06
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

### Διάλεξη 11: μνήμη και κόστος

| Αρχείο | Τι κάνει |
|---|---|
| pythia_memory.py | Κοινές συναρτήσεις: κλήση με καταγραφή κόστους, παράθυρο, σύνοψη |
| forget.py | Το μοντέλο δεν θυμάται· η μνήμη είναι το ιστορικό που ξαναστέλνουμε |
| growth.py | Πόσα tokens στέλνει κάθε γύρος, με τρεις στρατηγικές (χωρίς κλήση σε μοντέλο) |
| context_limit.py | Σιωπηλή περικοπή όταν το κείμενο δεν χωρά στο τοπικό μοντέλο |
| chat_memory.py | Συνομιλία με `--strategy full / window / summary`, `--auto`, `--budget` |
| cache_demo.py | Prompt caching με τον κατάλογο προϊόντων |
| costs_report.py | Σύνολα κόστους από το costs.csv |
| app_chat.py | API συνομιλίας με μνήμη ανά χρήστη (`uvicorn app_chat:app --reload`) |

### Διάλεξη 12: embeddings

| Αρχείο | Τι κάνει |
|---|---|
| pythia_embed.py | Κοινές συναρτήσεις: embeddings, ομοιότητα συνημιτόνου, FAQ |
| keyword_vs_meaning.py | Αναζήτηση με λέξεις και με νόημα, δίπλα-δίπλα |
| embed.py | Ένα κείμενο γίνεται διάνυσμα |
| similarity.py | Πίνακας ομοιότητας 6 προτάσεων |
| build_index.py | Το FAQ στη βάση Chroma (φάκελος db/) |
| search.py | Αναζήτηση στη βάση (`--k`, `--category`) |
| eval_search.py | hit@1 και hit@3 (`--model` για σύγκριση μοντέλων) |
| map2d.py | Το FAQ σε 2 διαστάσεις (map.png) |

Δεδομένα: `katalogos.txt`, `conversation.txt`, `faq.json`, `search_cases.json`. Όλα φανταστικά, για το e-shop «Μπρίκι».
Όλες οι εντολές με τη σειρά των διαφανειών: `questions.txt`.

### Για το project σας

Αντιγράψτε τον φάκελο, βάλτε τα δικά σας δεδομένα στο `faq.json` (πεδία id, category, question, answer),
και τρέξτε `build_index.py`, `search.py`, `eval_search.py`. Με το `embeddinggemma` τα δεδομένα δεν φεύγουν από τον υπολογιστή σας.

### Ασφάλεια

Το `.env` με τα κλειδιά δεν μπαίνει ποτέ σε zip, git ή κοινόχρηστο φάκελο. Το `costs.csv` δεν περιέχει κείμενα ή κλειδιά.
