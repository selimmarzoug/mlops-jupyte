# 🚀 GUIDE DE DÉPLOIEMENT GCP

## Prérequis

1. **Compte Google Cloud Platform**
   - Créer un compte: https://console.cloud.google.com
   - Activer la facturation (50$ de crédit disponible)
   - Créer un nouveau projet

2. **Installer Google Cloud SDK**
   ```bash
   # Linux
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   
   # macOS
   brew install --cask google-cloud-sdk
   
   # Vérifier
   gcloud --version
   ```

3. **Configuration initiale**
   ```bash
   # S'authentifier
   gcloud auth login
   
   # Lister vos projets
   gcloud projects list
   
   # Définir le projet
   gcloud config set project YOUR_PROJECT_ID
   ```

## Étapes de déploiement

### 1. Modifier le script deploy_gcp.sh

Ouvrir `deploy_gcp.sh` et modifier:
```bash
PROJECT_ID="your-gcp-project-id"  # Remplacer par votre Project ID
```

### 2. Exécuter le déploiement

```bash
cd deployment/
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

### 3. Tester l'API déployée

Une fois déployé, vous recevrez une URL comme:
```
https://playstore-model-api-xxxx-uc.a.run.app
```

Tester:
```bash
# Health check
curl https://YOUR_URL/health

# Info
curl https://YOUR_URL/info

# Prédiction
curl -X POST https://YOUR_URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [
      {
        "Rating": 4.5,
        "Reviews": 10000,
        "Size": 25.0,
        "Installs": 1000000,
        "Price": 0.0
      }
    ]
  }'
```

## Gestion des coûts

### Voir vos coûts actuels
```bash
gcloud billing accounts list
gcloud billing projects describe YOUR_PROJECT_ID
```

### Limiter les coûts
1. **Set budget alerts**: Console GCP > Billing > Budgets
2. **Limiter les instances**: `--max-instances 3`
3. **Scale to zero**: `--min-instances 0` (défaut)
4. **Supprimer quand inutilisé**: `gcloud run services delete SERVICE_NAME`

### Coûts estimés pour 50$

| Usage | Durée | Coût |
|-------|-------|------|
| Instance 24/7 | 20 mois | 50$ |
| 1000 req/jour | 2+ ans | 50$ |
| Dev/Test sporadique | Plusieurs années | 50$ |

**Recommandation**: Avec `--min-instances 0`, votre service sera quasi-gratuit!

## Monitoring

### Voir les logs
```bash
gcloud run services logs read playstore-model-api --limit=50
```

### Métriques dans la console
https://console.cloud.google.com/run

## Nettoyage

### Supprimer le service
```bash
gcloud run services delete playstore-model-api --region us-central1
```

### Supprimer l'image
```bash
gcloud container images delete gcr.io/PROJECT_ID/playstore-model-api
```

## Problèmes courants

### Erreur: "Permission denied"
```bash
gcloud auth login
gcloud auth configure-docker
```

### Erreur: "MLflow tracking URI not accessible"
- Le container ne peut pas accéder à votre MLflow local
- Solutions:
  1. Déployer MLflow sur GCP aussi
  2. Utiliser un modèle pré-chargé dans le container
  3. Utiliser ngrok pour exposer MLflow temporairement

### Erreur: "Out of memory"
```bash
# Augmenter la mémoire
gcloud run deploy SERVICE_NAME --memory 1Gi
```

## Ressources

- Documentation Cloud Run: https://cloud.google.com/run/docs
- Pricing: https://cloud.google.com/run/pricing
- Quotas: https://cloud.google.com/run/quotas
