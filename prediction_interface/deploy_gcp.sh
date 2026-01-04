#!/bin/bash
# Script de déploiement sur Google Cloud Run
# Usage: ./deploy_gcp.sh

set -e

# ============================================
# CONFIGURATION - MODIFIEZ CES VALEURS
# ============================================

PROJECT_ID="mlops-prediction-1767534299"
SERVICE_NAME="prediction-app"
REGION="europe-west1"  # Région Europe (Belgique)
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# ============================================
# VÉRIFICATIONS
# ============================================

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     🚀 DÉPLOIEMENT SUR GOOGLE CLOUD RUN 🚀              ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier si gcloud est installé
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK n'est pas installé"
    echo "📥 Installez-le: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ Google Cloud SDK détecté"

# Vérifier PROJECT_ID
if [ "$PROJECT_ID" == "votre-project-id" ]; then
    echo ""
    echo "⚠️  ATTENTION: Vous devez modifier PROJECT_ID dans ce script!"
    echo ""
    echo "1. Ouvrez ce fichier: deploy_gcp.sh"
    echo "2. Changez 'votre-project-id' par votre vrai PROJECT_ID"
    echo "3. Relancez le script"
    echo ""
    echo "Pour trouver votre PROJECT_ID:"
    echo "   gcloud projects list"
    exit 1
fi

# Configurer le projet
echo "📋 Configuration du projet: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# ============================================
# PRÉPARATION
# ============================================

echo ""
echo "📦 Préparation des fichiers..."

# Copier le modèle si disponible
if [ -f "../models/model.pkl" ]; then
    echo "✅ Copie du modèle model.pkl"
    cp ../models/model.pkl .
else
    echo "⚠️  Aucun modèle trouvé (sera chargé depuis MLflow)"
fi

# ============================================
# BUILD DE L'IMAGE DOCKER
# ============================================

echo ""
echo "🐳 Construction de l'image Docker..."
echo "   Image: $IMAGE_NAME"

gcloud builds submit --tag $IMAGE_NAME .

echo "✅ Image construite avec succès!"

# ============================================
# DÉPLOIEMENT SUR CLOUD RUN
# ============================================

echo ""
echo "🚀 Déploiement sur Cloud Run..."

gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --timeout 300 \
    --port 8080

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     ✅ DÉPLOIEMENT TERMINÉ! ✅                          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Récupérer l'URL du service
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo "🌐 Votre application est accessible à:"
echo ""
echo "   $SERVICE_URL"
echo ""
echo "📊 Tableau de bord Cloud Run:"
echo "   https://console.cloud.google.com/run?project=$PROJECT_ID"
echo ""
echo "💰 Estimation des coûts (pour 50$ de crédit):"
echo "   - Cloud Run: ~0.05$ par heure d'utilisation"
echo "   - Cloud Build: ~0.003$ par build"
echo "   - Container Registry: ~0.026$ par Go/mois"
echo ""
echo "   ➡️  Avec 50$, vous pouvez faire tourner l'app pendant ~1000 heures"
echo "      soit environ 40 jours en continu!"
echo ""
echo "🎯 Prochaines étapes:"
echo "   1. Testez votre application: $SERVICE_URL"
echo "   2. Surveillez les coûts: https://console.cloud.google.com/billing"
echo "   3. Configurez des alertes budgétaires"
echo ""
