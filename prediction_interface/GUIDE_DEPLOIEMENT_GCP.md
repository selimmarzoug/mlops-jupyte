# 🚀 Guide de Déploiement sur Google Cloud Platform

## 📋 Prérequis

- ✅ Compte Google Cloud Platform avec 50$ de crédit
- ✅ Carte bancaire (pour validation, mais aucun débit avec le crédit gratuit)
- ✅ Google Cloud SDK installé sur votre machine

---

## 🎯 ÉTAPE 1: Installer Google Cloud SDK

### Sur Linux/Ubuntu:

```bash
# Télécharger et installer
curl https://sdk.cloud.google.com | bash

# Redémarrer le terminal, puis initialiser
exec -l $SHELL
gcloud init
```

### Alternative (snap):
```bash
sudo snap install google-cloud-cli --classic
```

### Vérifier l'installation:
```bash
gcloud --version
```

---

## 🌐 ÉTAPE 2: Créer un Projet GCP

### Option A: Via la Console Web

1. Allez sur: https://console.cloud.google.com
2. Cliquez sur **"Sélectionner un projet"** en haut
3. Cliquez sur **"Nouveau projet"**
4. Nom du projet: `mlops-prediction-app`
5. Cliquez sur **"Créer"**
6. **Notez le PROJECT_ID** (exemple: `mlops-prediction-app-123456`)

### Option B: Via la Ligne de Commande

```bash
# Se connecter à Google Cloud
gcloud auth login

# Lister vos projets existants
gcloud projects list

# Créer un nouveau projet
gcloud projects create mlops-prediction-app-123456 --name="MLOps Prediction App"

# Noter le PROJECT_ID qui s'affiche
```

---

## 💳 ÉTAPE 3: Activer la Facturation

1. Allez sur: https://console.cloud.google.com/billing
2. Sélectionnez votre projet
3. Cliquez sur **"Associer un compte de facturation"**
4. Sélectionnez votre compte avec les 50$ de crédit gratuit
5. Confirmez

---

## 🔧 ÉTAPE 4: Activer les APIs Nécessaires

```bash
# Définir votre projet
gcloud config set project VOTRE-PROJECT-ID

# Activer Cloud Run API
gcloud services enable run.googleapis.com

# Activer Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Activer Container Registry API
gcloud services enable containerregistry.googleapis.com
```

**Via la console web:**
1. https://console.cloud.google.com/apis/library
2. Rechercher et activer: "Cloud Run API"
3. Rechercher et activer: "Cloud Build API"
4. Rechercher et activer: "Container Registry API"

---

## 📝 ÉTAPE 5: Configurer le Script de Déploiement

### Modifier le fichier deploy_gcp.sh:

```bash
cd /home/selim/mlops-jupyter/prediction_interface
nano deploy_gcp.sh
```

**Changez cette ligne:**
```bash
PROJECT_ID="votre-project-id"  # ⚠️ CHANGEZ CECI
```

**Par votre vrai PROJECT_ID:**
```bash
PROJECT_ID="mlops-prediction-app-123456"  # Votre PROJECT_ID réel
```

Sauvegardez: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 🚀 ÉTAPE 6: Déployer l'Application

```bash
cd /home/selim/mlops-jupyter/prediction_interface

# Lancer le déploiement
./deploy_gcp.sh
```

**Le script va:**
1. ✅ Vérifier les prérequis
2. 🐳 Construire l'image Docker (5-10 min)
3. 📦 L'uploader sur Google Container Registry
4. 🚀 Déployer sur Cloud Run
5. 🌐 Vous donner l'URL publique

---

## 🌐 ÉTAPE 7: Tester l'Application

Après le déploiement, vous recevrez une URL comme:
```
https://prediction-app-xxxxx-ew.a.run.app
```

Testez-la dans votre navigateur avec les mêmes valeurs qu'en local!

---

## 💰 ÉTAPE 8: Surveiller les Coûts

### Configurer une Alerte Budgétaire:

1. Allez sur: https://console.cloud.google.com/billing/budgets
2. Cliquez sur **"Créer un budget"**
3. Configurez:
   - Nom: `Alerte 50 dollars`
   - Budget: `50 USD`
   - Alertes à: 50%, 75%, 90%, 100%
4. Ajoutez votre email pour les notifications

### Estimer les Coûts:

**Cloud Run (pricing):**
- CPU: $0.00002400 par vCPU-seconde
- Mémoire: $0.00000250 par GiB-seconde
- Requêtes: $0.40 par million de requêtes
- **Inclus gratuitement chaque mois:**
  - 2 millions de requêtes
  - 360,000 vCPU-secondes
  - 180,000 GiB-secondes

**Avec 50$ de crédit:**
- ~1000 heures d'utilisation continue
- OU ~5-10 millions de requêtes
- **Suffisant pour 1-2 mois d'utilisation normale!**

---

## 🎛️ ÉTAPE 9: Commandes Utiles

### Voir les logs en temps réel:
```bash
gcloud run services logs read prediction-app --region=europe-west1 --follow
```

### Voir les détails du service:
```bash
gcloud run services describe prediction-app --region=europe-west1
```

### Mettre à jour après modifications:
```bash
cd /home/selim/mlops-jupyter/prediction_interface
./deploy_gcp.sh
```

### Arrêter le service (économiser du crédit):
```bash
gcloud run services delete prediction-app --region=europe-west1
```

### Redéployer plus tard:
```bash
./deploy_gcp.sh
```

---

## 🔒 ÉTAPE 10: Sécurité (Optionnel)

### Ajouter une authentification:

Si vous voulez restreindre l'accès:

```bash
# Supprimer l'accès public
gcloud run services remove-iam-policy-binding prediction-app \
    --region=europe-west1 \
    --member="allUsers" \
    --role="roles/run.invoker"

# Ajouter votre email
gcloud run services add-iam-policy-binding prediction-app \
    --region=europe-west1 \
    --member="user:votre-email@gmail.com" \
    --role="roles/run.invoker"
```

---

## ⚠️ DÉPANNAGE

### Erreur: "Project not found"
```bash
# Vérifier que votre projet existe
gcloud projects list

# Le sélectionner
gcloud config set project VOTRE-PROJECT-ID
```

### Erreur: "API not enabled"
```bash
# Activer toutes les APIs d'un coup
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com
```

### Erreur: "Permission denied"
```bash
# Se reconnecter
gcloud auth login
gcloud auth application-default login
```

### L'application ne démarre pas
```bash
# Voir les logs
gcloud run services logs read prediction-app --region=europe-west1 --limit=50
```

---

## 📊 Tableaux de Bord Utiles

- **Console Cloud Run:** https://console.cloud.google.com/run
- **Surveillance des coûts:** https://console.cloud.google.com/billing
- **Logs:** https://console.cloud.google.com/logs
- **Métriques:** https://console.cloud.google.com/monitoring

---

## ✅ Checklist de Déploiement

- [ ] Google Cloud SDK installé
- [ ] Compte GCP créé avec 50$ de crédit
- [ ] Projet créé et PROJECT_ID noté
- [ ] Facturation activée
- [ ] APIs activées (Cloud Run, Cloud Build, Container Registry)
- [ ] deploy_gcp.sh modifié avec votre PROJECT_ID
- [ ] Script exécuté: `./deploy_gcp.sh`
- [ ] URL de l'application reçue
- [ ] Application testée dans le navigateur
- [ ] Alerte budgétaire configurée

---

## 🎉 Résultat Final

Après toutes ces étapes, vous aurez:

✅ Une application de prédiction ML déployée publiquement
✅ Accessible via une URL HTTPS
✅ Auto-scaling (supporte jusqu'à 10 instances)
✅ Surveiller les coûts en temps réel
✅ ~1000 heures d'utilisation avec 50$

**URL finale:** `https://prediction-app-xxxxx-ew.a.run.app`

---

## 📞 Support

- Documentation Cloud Run: https://cloud.google.com/run/docs
- Forum GCP: https://stackoverflow.com/questions/tagged/google-cloud-run
- Pricing Calculator: https://cloud.google.com/products/calculator

Bon déploiement! 🚀
