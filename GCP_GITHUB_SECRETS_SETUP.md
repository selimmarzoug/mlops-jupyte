# Configuration des Secrets GitHub pour Déploiement GCP

## 📋 Secrets Requis

Vous devez configurer 2 secrets dans GitHub:

1. **GCP_PROJECT_ID**: Votre ID de projet Google Cloud
2. **GCP_SA_KEY**: Clé JSON du Service Account

---

## 🔧 Étape 1: Créer un Service Account

```bash
# Créer le service account
gcloud iam service-accounts create github-actions-deployer \
    --display-name="GitHub Actions Deployer" \
    --project=mlops-prediction-1767534299

# Donner les permissions nécessaires
gcloud projects add-iam-policy-binding mlops-prediction-1767534299 \
    --member="serviceAccount:github-actions-deployer@mlops-prediction-1767534299.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding mlops-prediction-1767534299 \
    --member="serviceAccount:github-actions-deployer@mlops-prediction-1767534299.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding mlops-prediction-1767534299 \
    --member="serviceAccount:github-actions-deployer@mlops-prediction-1767534299.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding mlops-prediction-1767534299 \
    --member="serviceAccount:github-actions-deployer@mlops-prediction-1767534299.iam.gserviceaccount.com" \
    --role="roles/storage.admin"
```

---

## 🔑 Étape 2: Créer et Télécharger la Clé

```bash
# Créer la clé JSON
gcloud iam service-accounts keys create ~/gcp-github-key.json \
    --iam-account=github-actions-deployer@mlops-prediction-1767534299.iam.gserviceaccount.com \
    --project=mlops-prediction-1767534299

# Afficher le contenu (pour copier)
cat ~/gcp-github-key.json
```

⚠️ **Important**: Copiez tout le contenu du fichier JSON (y compris les accolades `{}`)

---

## 🔐 Étape 3: Ajouter les Secrets dans GitHub

### Via l'Interface Web:

1. Allez sur votre repo: https://github.com/selimmarzoug/mlops-jupyte

2. Cliquez sur **Settings** → **Secrets and variables** → **Actions**

3. Cliquez sur **New repository secret**

4. Ajoutez le premier secret:
   - **Name**: `GCP_PROJECT_ID`
   - **Value**: `mlops-prediction-1767534299`
   - Cliquez **Add secret**

5. Ajoutez le deuxième secret:
   - **Name**: `GCP_SA_KEY`
   - **Value**: Collez tout le contenu du fichier JSON
   - Cliquez **Add secret**

### Via GitHub CLI (Alternative):

```bash
# Installer gh si nécessaire
# sudo snap install gh

gh auth login

# Ajouter GCP_PROJECT_ID
gh secret set GCP_PROJECT_ID --body "mlops-prediction-1767534299" --repo selimmarzoug/mlops-jupyte

# Ajouter GCP_SA_KEY
gh secret set GCP_SA_KEY < ~/gcp-github-key.json --repo selimmarzoug/mlops-jupyte
```

---

## ✅ Étape 4: Vérifier la Configuration

Une fois les secrets ajoutés:

1. Faites un commit et push:
   ```bash
   git add .
   git commit -m "feat: Add GCP auto-deployment to GitHub Actions"
   git push
   ```

2. Allez sur: https://github.com/selimmarzoug/mlops-jupyte/actions

3. Le workflow devrait se déclencher automatiquement

4. Le job **🚀 Déploiement GCP** apparaîtra après la finalisation

---

## 🎯 Fonctionnement

Le déploiement automatique se déclenche **uniquement**:
- ✅ Sur la branche `main`
- ✅ Quand le push est fait (pas sur PR)
- ✅ Après que tous les tests passent

**Pipeline complet:**
```
🤖 Entraînement ML
    ↓
📂 Vérification
    ↓
🐳 Build Docker
    ↓
🧪 Test Docker
    ↓
📦 Finalisation
    ↓
🚀 Déploiement GCP (auto!)
```

---

## 🔒 Sécurité

⚠️ **IMPORTANT**:

1. **Ne committez JAMAIS** le fichier `~/gcp-github-key.json` dans git!
2. Supprimez-le après configuration:
   ```bash
   rm ~/gcp-github-key.json
   ```
3. Les secrets GitHub sont chiffrés et sécurisés
4. Seul GitHub Actions peut les lire

---

## 🐛 Troubleshooting

### Erreur: "Permission denied"
➡️ Vérifiez que le Service Account a les rôles nécessaires

### Erreur: "Invalid credentials"
➡️ Vérifiez que vous avez copié TOUT le JSON (avec `{` et `}`)

### Le job ne se déclenche pas
➡️ Vérifiez que:
- Vous êtes sur la branche `main`
- C'est un `push` (pas une PR)
- Les secrets sont bien nommés `GCP_PROJECT_ID` et `GCP_SA_KEY`

---

## 💰 Coûts

Le déploiement automatique utilise:
- Cloud Build: ~0.003$ par build (première 120 builds/jour gratuits)
- Cloud Run: Même coût que le déploiement manuel

Avec votre crédit de 50$, vous pouvez faire **des centaines de déploiements**! 💪
