# Πώς τρέχετε τα scripts στα Windows

## 1. Αντιγράψτε τον φάκελο εκτός Google Drive

Αντιγράψτε τον φάκελο `code` π.χ. στο `C:\ai4dev`. Το εικονικό περιβάλλον της Python (venv) έχει χιλιάδες μικρά αρχεία και το Drive θα προσπαθεί να τα συγχρονίζει. Επίσης το `.env` με το κλειδί σας δεν πρέπει να βρίσκεται σε κοινόχρηστο φάκελο.

## 2. Εγκαταστήστε

- Python 3.13 από το python.org. Στην εγκατάσταση τσεκάρετε το «Add Python to PATH».
- Ollama από το ollama.com.

## 3. Στήστε το περιβάλλον (PowerShell)

Αν το `python` ανοίγει το Microsoft Store ή βγάζει «Python was not found»: Ρυθμίσεις → Εφαρμογές → Ρυθμίσεις για προχωρημένους → Ψευδώνυμα εκτέλεσης εφαρμογών, και κλείστε τα python.exe / python3.exe. Μετά ξανανοίξτε το terminal.

Οι ίδιες εντολές δουλεύουν και στο Command Prompt (cmd), που είναι συχνά το terminal του PyCharm.

```powershell
cd C:\ai4dev
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env
```

Αν το `activate` βγάλει σφάλμα για execution policy, τρέξτε πρώτα:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 4. Το αρχείο .env

- Βασικό κλειδί: Anthropic (Claude) από το platform.claude.com → Settings → API keys, στη γραμμή `ANTHROPIC_API_KEY=`. Χρειάζεται υπόλοιπο σε credits (Billing). Βάλτε και όριο δαπανών.
- Προαιρετικά Gemini (aistudio.google.com, δωρεάν αλλά με χαμηλό ημερήσιο όριο) στη γραμμή `GEMINI_API_KEY=`.
- Για το `next_token.py` χρειάζεστε και κλειδί OpenAI (`OPENAI_API_KEY=`).
- Στη γραμμή `ARENA_MODELS` κρατήστε μόνο μοντέλα για τα οποία έχετε κλειδί. Μόνο με Claude:
  `ARENA_MODELS=anthropic/claude-haiku-5-5,ollama_chat/gemma3:4b,ollama_chat/llama3.2:1b`

## 5. Τοπικά μοντέλα (μία φορά, περίπου 4,5 GB)

```powershell
ollama pull gemma3:4b
ollama pull llama3.2:1b
```

## 6. Δοκιμή

```powershell
python ask.py "Πες μου κάτι για τον Τάλω"
python ask.py --local "Πες μου κάτι για τον Τάλω"
python arena.py "Εξήγησε τι είναι ένα LLM σε έναν παππού από την Κρήτη"
```

Κάθε φορά που ανοίγετε νέο PowerShell, πριν τρέξετε κάτι:

```powershell
cd C:\ai4dev
.venv\Scripts\activate
```

Αν μια κλήση αποτύχει με «model not found», το όνομα του μοντέλου έχει αλλάξει από τον πάροχο. Διορθώστε τη γραμμή `MODEL=` στο `.env`.

## Τι κάνει κάθε script

| Script | Διάλεξη | Τι κάνει |
|---|---|---|
| `tokens.py` | 1 | Πόσα tokens θέλει η ίδια πρόταση στα ελληνικά και στα αγγλικά. Με όρισμα δείχνει πώς κόβεται μια λέξη: `python tokens.py Θεσσαλονίκη` |
| `next_token.py` | 1 | Οι 10 πιθανότερες επόμενες λέξεις με την πιθανότητά τους. Θέλει κλειδί OpenAI |
| `chatbot.py` | 1 | Chatbot με μνήμη σε 7 γραμμές. Γράψτε «τέλος» για έξοδο |
| `ask.py` | 2 | Μία ερώτηση: απάντηση, χρόνος, tokens, κόστος. Με `--local` απαντά το τοπικό μοντέλο |
| `pythia.py` | 2 | Το ίδιο μοντέλο με τρεις προσωπικότητες |
| `temperature.py` | 2 | Η ίδια ερώτηση 4 φορές με temperature 0 και 4 φορές με 1 |
| `stream.py` | 2 | Η απάντηση εμφανίζεται καθώς γράφεται, με τον χρόνο μέχρι την πρώτη λέξη |
| `arena.py` | 2 | Τυφλή σύγκριση μοντέλων: απαντήσεις Α, Β, Γ, ψηφοφορία, αποκάλυψη με Enter |
