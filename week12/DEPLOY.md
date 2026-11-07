# Η Πυθία στο cloud · τρεις δρόμοι

Ο κώδικας είναι ο ίδιος με την εβδομάδα 11 (Dockerfile, app.py). Αλλάζουν τρία πράγματα:
πού χτίζεται η εικόνα, πού ζουν τα κλειδιά, και πώς γίνονται τα embeddings.

> Οι εντολές ελέγχθηκαν με την τεκμηρίωση των παρόχων τον Οκτώβριο του 2026 (όχι με πραγματική εγκατάσταση).
> Οι υπηρεσίες, οι τιμές και τα δωρεάν όρια αλλάζουν: ελέγξτε τα πριν. **Σβήστε ό,τι δεν χρειάζεστε μετά.**

## 0. Πριν από οποιονδήποτε δρόμο

### Embeddings χωρίς Ollama

Στο cloud δεν υπάρχει Ollama. Δύο λύσεις:

1. **Μοντέλο embeddings μέσω API** (απλούστερο). Π.χ. Gemini ή OpenAI (εβδομάδα 6). Η βάση πρέπει
   να ξαναφτιαχτεί **με το ίδιο μοντέλο**, πριν από το build:
   ```
   $env:EMBED_MODEL="gemini/gemini-embedding-001"     # θέλει GEMINI_API_KEY στο .env
   Remove-Item -Recurse db
   python ingest.py
   ```
   Και στο cloud ορίζετε `EMBED_MODEL` με την ίδια τιμή (και το κλειδί του).
2. **Ollama σε δικό του container / VM** με αρκετή μνήμη, και `OLLAMA_API_BASE` προς αυτό. Ακριβότερο και πιο σύνθετο.

### Κλειδί της εφαρμογής

Μια δημόσια διεύθυνση = ο καθένας μπορεί να ξοδέψει τα λεφτά σας. Ορίστε **`APP_TOKEN`** (ένα τυχαίο κείμενο)
στο cloud: το `/chat` θα θέλει την κεφαλίδα `X-Token`. Για τα scripts: `$env:APP_TOKEN="..."` στο terminal.

### Όριο δαπάνης

Ξεχωριστό κλειδί Anthropic για την παραγωγή, με **όριο δαπάνης** στην κονσόλα.

---

## Δρόμος Α · Azure Container Apps

Προαπαιτούμενα: λογαριασμός Azure, Azure CLI.

```
az login
az upgrade
az extension add --name containerapp --upgrade --allow-preview true
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

$RG="pythia-rg"; $LOC="westeurope"; $ENVNAME="pythia-env"; $APP="pythia"
az group create --name $RG --location $LOC

# Χτίζει την εικόνα από το Dockerfile ΑΥΤΟΥ του φακέλου και την εγκαθιστά (η θύρα από το EXPOSE 8000).
az containerapp up --name $APP --resource-group $RG --location $LOC --environment $ENVNAME --source .
```

Κλειδιά ως **secrets** (όχι ως απλές μεταβλητές):

```
az containerapp secret set --name $APP --resource-group $RG --secrets anthropic-key=<ΚΛΕΙΔΙ> gemini-key=<ΚΛΕΙΔΙ> app-token=<ΤΥΧΑΙΟ> salt=<ΤΥΧΑΙΟ>
az containerapp update --name $APP --resource-group $RG --set-env-vars ANTHROPIC_API_KEY=secretref:anthropic-key GEMINI_API_KEY=secretref:gemini-key APP_TOKEN=secretref:app-token PSEUDO_SALT=secretref:salt EMBED_MODEL=gemini/gemini-embedding-001 APP_VERSION=1.0 LOG_STDOUT=1
```

Η διεύθυνση: `az containerapp show --name $APP --resource-group $RG --query properties.configuration.ingress.fqdn`.
Σβήσιμο **όλων**: `az group delete --name $RG`.

## Δρόμος Β · Google Cloud Run

Προαπαιτούμενα: project με billing, gcloud CLI (`gcloud init`).

```
gcloud services enable run.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com

# Κλειδιά στο Secret Manager (η τιμή από το stdin, όχι στο ιστορικό).
"<ΚΛΕΙΔΙ>" | gcloud secrets create anthropic-key --data-file=-
"<ΚΛΕΙΔΙ>" | gcloud secrets create gemini-key --data-file=-
"<ΤΥΧΑΙΟ>" | gcloud secrets create app-token --data-file=-

# Χτίζει από το Dockerfile και εγκαθιστά. Η εφαρμογή ακούει στη θύρα 8000.
gcloud run deploy pythia --source . --region europe-west1 --port 8000 --allow-unauthenticated `
  --set-secrets ANTHROPIC_API_KEY=anthropic-key:latest,GEMINI_API_KEY=gemini-key:latest,APP_TOKEN=app-token:latest `
  --set-env-vars EMBED_MODEL=gemini/gemini-embedding-001,APP_VERSION=1.0,LOG_STDOUT=1
```

Ο λογαριασμός υπηρεσίας του Cloud Run χρειάζεται δικαίωμα «Secret Manager Secret Accessor».
Σβήσιμο: `gcloud run services delete pythia --region europe-west1`.

## Δρόμος Γ · Render (απλούστερο, με περιορισμούς)

Νέο Web Service από το GitHub repository σας, με τον Dockerfile. Κλειδιά στα Environment Variables / Secret Files.
Δωρεάν instances: «κοιμούνται» μετά από 15 λεπτά χωρίς κίνηση (ξυπνούν σε ~1 λεπτό), 750 ώρες/μήνα,
χωρίς μόνιμο δίσκο: **τα logs χάνονται** σε κάθε επανεκκίνηση. Για demo αρκεί· για παραγωγή, όχι.

---

## Μετά την εγκατάσταση

```
$env:APP_TOKEN="<ΤΟ ΙΔΙΟ ΜΕ ΤΟ CLOUD>"
python release_check.py https://<η-διεύθυνσή-σας>
```

Τα logs: στο cloud το σύστημα αρχείων του container δεν είναι μόνιμο. Με `LOG_STDOUT=1` κάθε γραμμή πάει και στα logs
της υπηρεσίας (Azure: Log Analytics · Cloud Run: Cloud Logging). Σε παραγωγή: μόνιμος αποθηκευτικός χώρος ή σύστημα logs.
