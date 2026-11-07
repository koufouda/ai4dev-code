# Εβδομάδα 7 · RAG

Κώδικας για τις διαλέξεις 13 (εισαγωγή και επεξεργασία εγγράφων) και 14 (βελτίωση ανάκτησης).

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

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive/OneDrive. Αντιγράψτε αυτόν τον φάκελο μέσα του ως `week07`.

Windows (PowerShell):

```powershell
cd C:\ai4dev
python -m venv .venv          # μόνο την πρώτη φορά
.venv\Scripts\activate
pip install -r week07\requirements.txt
cd week07
python check.py
```

Linux:

```bash
cd ~/ai4dev
python3 -m venv .venv         # μόνο την πρώτη φορά
source .venv/bin/activate
pip install -r week07/requirements.txt
cd week07
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

### Τα έγγραφα (docs/)

Τέσσερα φανταστικά έγγραφα του e-shop «Μπρίκι»: εγχειρίδιο της μηχανής ΜΠ-001 (PDF), πολιτική εγγύησης και service (PDF),
όροι πώλησης (Word), πολιτική απορρήτου (Word). Βάλτε δίπλα τους τα δικά σας PDF ή Word και τρέξτε ξανά το `ingest.py`.

### Διάλεξη 13

| Αρχείο | Τι κάνει |
|---|---|
| pythia_rag.py | Όλες οι κοινές συναρτήσεις (διάβασμα, καθάρισμα, κομμάτια, βάση, αναζήτηση, απάντηση) |
| no_rag.py | Η Πυθία χωρίς έγγραφα |
| read_doc.py | Τι «βλέπει» η Python σε ένα PDF ή Word |
| clean_demo.py | Πριν και μετά το καθάρισμα |
| chunk_demo.py | Πώς κόβουμε σε κομμάτια (`--naive`, `--size`, `--overlap`, `--file`) |
| ingest.py | Όλα τα έγγραφα στη βάση |
| ask.py | Ερωτήσεις στα έγγραφα (`--show`, `--method`, `--rerank`, `--k`) |
| app_rag.py | API: `/upload` και `/ask` (`uvicorn app_rag:app --reload`) |

### Διάλεξη 14

| Αρχείο | Τι κάνει |
|---|---|
| compare.py | Η ίδια ερώτηση με vector, BM25, hybrid |
| bm25_demo.py | Αναζήτηση λέξεων και κανονικοποίηση για ελληνικά |
| rerank_demo.py | Reranking με LLM |
| eval_retrieval.py | hit@1, hit@k, MRR στο `rag_cases.json` (`--all`, `--method`, `--rerank`, `--size`, `--no-stem`) |

Όλες οι εντολές με τη σειρά των διαφανειών: `questions.txt`.

### Για το project σας

Αντιγράψτε τον φάκελο, βάλτε τα δικά σας έγγραφα στο `docs/`, γράψτε τις δοκιμές σας στο `rag_cases.json`
(ερώτηση, φράση που πρέπει να υπάρχει στο σωστό κομμάτι, αρχείο) και τρέξτε `python eval_retrieval.py --all`.

### Ασφάλεια

Χωρίς προσωπικά ή εμπιστευτικά έγγραφα. Τα embeddings γίνονται τοπικά, αλλά τα κομμάτια που βρίσκει η αναζήτηση
στέλνονται στο μοντέλο συνομιλίας για την απάντηση. Το `.env` δεν μπαίνει ποτέ σε zip ή κοινόχρηστο φάκελο.
