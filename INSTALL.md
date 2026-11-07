# Εγκατάσταση προγραμμάτων

*AI for Developers · τι χρειάζεται στο PC σας · Windows 11 και Linux*

## Τι χρειάζεστε

Εγκαταστήστε τα πριν από το πρώτο μάθημα (Σάββατο 7/11). Το Docker και τα εργαλεία cloud χρειάζονται αργότερα, αλλά καλό είναι να τα στήσετε νωρίς, γιατί το Docker στα Windows θέλει επανεκκίνηση και μερικές φορές ρύθμιση στο BIOS.

| Πρόγραμμα | Για ποιο λόγο | Από | Υποχρεωτικό |
|---|---|---|---|
| Python 3.13 | Όλος ο κώδικας του μαθήματος | Μάθημα 1 | Ναι |
| Visual Studio Code<br>+ Python, Pylance | Επεξεργαστής κώδικα και τερματικό | Μάθημα 1 | Ναι |
| Ollama<br>+ τοπικά μοντέλα | Μοντέλα που τρέχουν στο δικό σας PC, χωρίς κλειδί και χωρίς κόστος | Μάθημα 2 | Ναι |
| Git | Εκδόσεις του κώδικα, GitHub, αυτόματοι έλεγχοι (CI) | Μάθημα 21 | Ναι |
| Docker | Πακετάρισμα της εφαρμογής σε container | Μάθημα 21 | Ναι |
| Claude Desktop | Σύνδεση της Πυθίας με εφαρμογή μέσω MCP | Μάθημα 19 | Προαιρετικό |
| Node.js (LTS) | Μόνο για το MCP Inspector (npx) | Μάθημα 19 | Προαιρετικό |
| Azure CLI ή Google Cloud CLI | Εγκατάσταση της εφαρμογής στο cloud (ένα από τα δύο, ή κανένα αν διαλέξετε Render) | Μάθημα 23 | Προαιρετικό |

### Υπολογιστής

- Windows 11 ή Linux 64-bit (Ubuntu 22.04/24.04, Debian 12, Fedora κ.λπ.).
- Μνήμη: 16 GB προτείνονται, 8 GB το ελάχιστο. Με 8 GB τα τοπικά μοντέλα είναι αργά και θα χρησιμοποιείτε κυρίως τα μικρότερα.
- Ελεύθερος χώρος: περίπου 25 GB (μοντέλα Ollama περίπου 10 GB, Docker 5-10 GB, πακέτα Python 2 GB).
- Δικαιώματα διαχειριστή (administrator / sudo) για τις εγκαταστάσεις. Σε εταιρικό laptop ρωτήστε πρώτα το IT, κυρίως για το Docker.

### Λογαριασμοί

| Λογαριασμός | Πού | Σημείωση |
|---|---|---|
| Anthropic (Claude API) | platform.claude.com → Settings → API keys | Το βασικό κλειδί του μαθήματος. Χρειάζεται υπόλοιπο σε credits (Billing). Βάλτε όριο δαπάνης. |
| GitHub | github.com | Δωρεάν. Για το repository και τους αυτόματους ελέγχους (μάθημα 21). |
| Gemini (προαιρετικό) | aistudio.google.com | Δωρεάν κλειδί με ημερήσιο όριο. Χρήσιμο για σύγκριση μοντέλων και για embeddings στο cloud. |
| OpenAI (προαιρετικό) | platform.openai.com | Μόνο για το next_token.py του μαθήματος 1 και για σύγκριση. |
| Cloud (μάθημα 23) | Azure, Google Cloud ή Render | Ένας από τους τρεις. Ελέγξτε τα δωρεάν όρια πριν βάλετε κάρτα. |

> **Τα κλειδιά σας**
>
> - Τα κλειδιά API μπαίνουν μόνο στο αρχείο .env του φακέλου του μαθήματος (π.χ. C:\ai4dev\.env ή ~/ai4dev/.env).
> - Όχι σε Google Drive, OneDrive ή Dropbox, όχι σε email ή chat, όχι σε GitHub, και ποτέ στην οθόνη όταν μοιράζεστε την οθόνη σας.
> - Αν ένα κλειδί διαρρεύσει, ακυρώστε το αμέσως από την κονσόλα και φτιάξτε νέο.

## Εγκατάσταση στα Windows 11

Κάθε βήμα έχει δύο τρόπους: από τη σελίδα του προγράμματος, ή με μία εντολή winget στο PowerShell. Ο δεύτερος είναι γρηγορότερος. Ανοίξτε το PowerShell από το μενού Έναρξη (γράψτε PowerShell).

### 1. Python 3.13

1. Κατεβάστε την Python 3.13 από το python.org/downloads (Windows installer 64-bit). Μη διαλέξετε την 3.14: κάποια πακέτα του μαθήματος (chromadb) δεν δουλεύουν ακόμα σωστά σε αυτή.
2. Στην πρώτη οθόνη της εγκατάστασης τσεκάρετε **«Add python.exe to PATH»** και πατήστε Install Now.
3. Στο τέλος, αν εμφανιστεί «Disable path length limit», πατήστε το.

Ή με winget:

```
winget install -e --id Python.Python.3.13
```

Κλείστε και ξανανοίξτε το PowerShell και ελέγξτε:

```
python --version
```

Αν ανοίξει το Microsoft Store ή βγει «Python was not found»: Ρυθμίσεις → Εφαρμογές → Ρυθμίσεις για προχωρημένους → Ψευδώνυμα εκτέλεσης εφαρμογών (App execution aliases) και κλείστε τα δύο «python.exe» και «python3.exe». Ξανανοίξτε το PowerShell.

### 2. Visual Studio Code

1. Κατεβάστε από το code.visualstudio.com (User Installer). Στην εγκατάσταση τσεκάρετε «Add to PATH» και «Add "Open with Code" action».
2. Ανοίξτε το VS Code, πατήστε Ctrl+Shift+X και εγκαταστήστε το **Python** (Microsoft). Μαζί του έρχονται το **Pylance** και το **Python Debugger**.

```
winget install -e --id Microsoft.VisualStudioCode
```

### 3. Git

1. Κατεβάστε από το git-scm.com/download/win και αφήστε τις προεπιλογές.
2. Ορίστε όνομα και email (ίδιο με του GitHub):

```
winget install -e --id Git.Git
git config --global user.name "Όνομα Επώνυμο"
git config --global user.email "to-email-sas@example.com"
```

### 4. Ollama και τοπικά μοντέλα

1. Κατεβάστε το OllamaSetup.exe από το ollama.com/download και εγκαταστήστε. Τρέχει στο παρασκήνιο (εικονίδιο κάτω δεξιά).
2. Κατεβάστε τα μοντέλα (μία φορά, θέλει χρόνο):

```
winget install -e --id Ollama.Ollama
ollama pull gemma3:4b
ollama pull llama3.2:1b
ollama pull embeddinggemma
```

Στο μάθημα 20 θα χρειαστούν και τα qwen3.5:4b και gemma4:e2b. Θα δοθούν τότε οι ακριβείς εντολές, γιατί τα ονόματα των μοντέλων αλλάζουν συχνά.

### 5. Docker Desktop

1. Το Docker στα Windows χρειάζεται WSL 2. Σε PowerShell ως διαχειριστής (δεξί κλικ → Run as administrator): **wsl --install** και επανεκκίνηση.
2. Κατεβάστε το Docker Desktop από το docker.com/products/docker-desktop και εγκαταστήστε με την επιλογή «Use WSL 2».
3. Ανοίξτε το Docker Desktop μία φορά και αποδεχτείτε τους όρους. Πρέπει να είναι ανοιχτό κάθε φορά που χρησιμοποιείτε το docker.
4. Αν βγει μήνυμα ότι λείπει η εικονικοποίηση (virtualization), ενεργοποιήστε την στο BIOS (Intel VT-x ή AMD-V/SVM).

```
wsl --install
winget install -e --id Docker.DockerDesktop
```

### 6. Προαιρετικά

- **Claude Desktop** (μάθημα 19): claude.ai/download.
- **Node.js LTS** (μάθημα 19, για το MCP Inspector): nodejs.org ή winget install -e --id OpenJS.NodeJS.LTS
- **Azure CLI** (μάθημα 23): winget install -e --id Microsoft.AzureCLI
- **Google Cloud CLI** (μάθημα 23): cloud.google.com/sdk/docs/install ή winget install -e --id Google.CloudSDK

## Εγκατάσταση σε Linux

Οι εντολές είναι για Ubuntu/Debian. Για Fedora υπάρχει σημείωση όπου διαφέρει. Ανοίξτε ένα τερματικό (Ctrl+Alt+T).

### 1. Python

Το Ubuntu 24.04 έχει την Python 3.12 και το Debian 12 την 3.11, που αρκούν. Χρειάζεται όμως το πακέτο για εικονικά περιβάλλοντα:

```
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version
```

Στο Linux η εντολή είναι python3. Μέσα στο εικονικό περιβάλλον (.venv) δουλεύει και το python, όπως στις οδηγίες του μαθήματος.

Fedora: οι νέες εκδόσεις έχουν Python 3.14 ως προεπιλογή. Εγκαταστήστε την 3.13 δίπλα της με **sudo dnf install python3.13** και φτιάξτε το περιβάλλον με python3.13 -m venv .venv.

### 2. Visual Studio Code

Κατεβάστε το .deb (Ubuntu/Debian) ή το .rpm (Fedora) από το code.visualstudio.com και ανοίξτε το, ή:

```
sudo apt install -y ./code_*.deb      # από τον φάκελο Λήψεις
# ή
sudo snap install code --classic
```

Μετά: Ctrl+Shift+X → Python (Microsoft).

### 3. Git

```
sudo apt install -y git
git config --global user.name "Όνομα Επώνυμο"
git config --global user.email "to-email-sas@example.com"
```

### 4. Ollama και τοπικά μοντέλα

```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma3:4b
ollama pull llama3.2:1b
ollama pull embeddinggemma
```

Το Ollama τρέχει ως υπηρεσία. Αν δεν απαντά: sudo systemctl start ollama.

### 5. Docker Engine

Στο Linux αρκεί το Docker Engine (χωρίς Docker Desktop). Ο πιο απλός τρόπος είναι το επίσημο script, και μετά προσθέτετε τον χρήστη σας στην ομάδα docker για να μη χρειάζεται sudo:

```
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# αποσυνδεθείτε και ξανασυνδεθείτε, μετά:
docker run hello-world
```

Για το docker compose: στο Ubuntu/Debian έρχεται μαζί (docker compose version για έλεγχο).

### 6. Προαιρετικά

- **Claude Desktop** (μάθημα 19): υπάρχει έκδοση beta για Ubuntu/Debian στο claude.ai/download. Αν δεν τη χρησιμοποιήσετε, το mcp_client.py του μαθήματος κάνει την ίδια δουλειά.
- **Node.js LTS** (μάθημα 19): από το nodejs.org (ή sudo apt install nodejs npm, αλλά η έκδοση του Ubuntu είναι συχνά παλιά).
- **Azure CLI** (μάθημα 23): curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
- **Google Cloud CLI** (μάθημα 23): οδηγίες στο cloud.google.com/sdk/docs/install

## Ο φάκελος του μαθήματος

Ένας φάκελος για όλο το μάθημα, **εκτός** Google Drive, OneDrive ή Dropbox: το εικονικό περιβάλλον έχει χιλιάδες αρχεία και το .env περιέχει τα κλειδιά σας.

| Βήμα | Windows 11 (PowerShell) | Linux (τερματικό) |
|---|---|---|
| Φάκελος | mkdir C:\ai4dev<br>cd C:\ai4dev | mkdir ~/ai4dev<br>cd ~/ai4dev |
| Εικονικό περιβάλλον | python -m venv .venv | python3 -m venv .venv |
| Ενεργοποίηση | .venv\Scripts\activate | source .venv/bin/activate |
| Πακέτα | pip install -r requirements.txt | pip install -r requirements.txt |
| Κλειδιά | copy .env.example .env<br>notepad .env | cp .env.example .env<br>nano .env |

Το requirements.txt και το .env.example υπάρχουν στον κώδικα κάθε εβδομάδας. Κάθε φορά που ανοίγετε νέο τερματικό, μπαίνετε στον φάκελο και ενεργοποιείτε το περιβάλλον. Στην αρχή της γραμμής πρέπει να φαίνεται (.venv).

Windows: αν το activate βγάλει σφάλμα για «execution policy», τρέξτε μία φορά **Set-ExecutionPolicy -Scope CurrentUser RemoteSigned** και ξαναδοκιμάστε.

### Στο VS Code

1. File → Open Folder και διαλέξτε τον φάκελο του μαθήματος (ολόκληρο τον φάκελο, όχι ένα αρχείο).
2. Ctrl+Shift+P. Στην μπάρα που ανοίγει πρέπει να φαίνεται το σύμβολο **>** στην αρχή. Αν λείπει, γράψτε το. Μετά γράψτε **Python: Select Interpreter** και Enter.
3. Διαλέξτε αυτόν που γράφει .venv. Κάτω δεξιά πρέπει να φαίνεται κάτι σαν 3.13.x ('.venv').

## Έλεγχος ότι όλα δουλεύουν

Σε νέο τερματικό. Κάθε εντολή πρέπει να τυπώσει μια έκδοση και όχι σφάλμα.

| Εντολή | Τι περιμένουμε |
|---|---|
| python --version  (Linux: python3 --version) | Python 3.11 ή νεότερη (στα Windows 3.13.x) |
| code --version | Έκδοση του VS Code |
| git --version | git version 2.x |
| ollama list | Τα μοντέλα gemma3:4b, llama3.2:1b, embeddinggemma |
| ollama run llama3.2:1b "Γεια σου" | Μια απάντηση από το τοπικό μοντέλο |
| docker run hello-world | «Hello from Docker!» |
| python check.py  (μέσα στο .venv) | Όλα ✓ (το check.py είναι στον κώδικα της εβδομάδας) |

Το check.py δείχνει μόνο αν υπάρχει κλειδί στο .env, ποτέ την τιμή του.

## Συχνά προβλήματα

| Πρόβλημα | Λύση |
|---|---|
| Windows: «python» ανοίγει το Microsoft Store | Κλείστε τα ψευδώνυμα εκτέλεσης για python.exe/python3.exe (Ρυθμίσεις → Εφαρμογές → Ρυθμίσεις για προχωρημένους). |
| «pip» ή «python» δεν βρίσκεται μετά την εγκατάσταση | Κλείστε και ξανανοίξτε το τερματικό (και το VS Code). Αν συνεχίζει, ξαναεγκαταστήστε την Python με «Add to PATH». |
| Linux: «ensurepip is not available» | sudo apt install python3-venv και ξαναφτιάξτε το .venv. |
| pip install αποτυγχάνει στο chromadb | Ελέγξτε ότι η Python είναι 3.11-3.13 (όχι 3.14). Σβήστε το .venv και φτιάξτε το ξανά με τη σωστή έκδοση. |
| VS Code: «No matching results» στο Python: Select Interpreter | Λείπει το > στην αρχή της μπάρας. Γράψτε >Python: Select Interpreter ή πατήστε F1. |
| ollama: «could not connect» | Windows: ανοίξτε το Ollama από το μενού Έναρξη. Linux: sudo systemctl start ollama. |
| Docker: «cannot connect to the Docker daemon» | Windows: ανοίξτε το Docker Desktop και περιμένετε να γράψει «Engine running». Linux: αποσυνδεθείτε/συνδεθείτε μετά το usermod, ή sudo systemctl start docker. |
| Docker Desktop: «Virtualization support not detected» | Ενεργοποιήστε VT-x/AMD-V στο BIOS και βεβαιωθείτε ότι έχει τρέξει το wsl --install. |
