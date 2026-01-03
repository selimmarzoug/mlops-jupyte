#!/bin/bash
# Script de déploiement sur Google Cloud Run
# Usage: ./deploy_gcp.sh

set -e  # Arrêter en cas d'erreur

# Configuration
PROJECT_ID="your-gcp-project-id"  # À MODIFIER
REGION="us-central1"  # Région la moins chère
SERVICE_NAME="playstore-model-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "======================================"
echo "🚀 Déploiement sur Google Cloud Run"
echo "======================================"
echo ""

# 1. Vérifier gcloud CLI
echo "📋 1/7 - Vérification de gcloud CLI..."
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI non installé"
    echo "   Installer: https://cloud.google.com/sdk/docs/install"
    exit 1
fi
echo "✅ gcloud CLI détecté"
echo ""

# 2. Authentification
echo "🔐 2/7 - Authentification GCP..."
gcloud auth login
gcloud config set project ${PROJECT_ID}
echo "✅ Authentifié sur projet: ${PROJECT_ID}"
echo ""

# 3. Activer les APIs nécessaires
echo "⚙️  3/7 - Activation des APIs GCP..."
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
echo "✅ APIs activées"
echo ""

# 4. Configurer Docker pour GCR
echo "🐳 4/7 - Configuration Docker..."
gcloud auth configure-docker
echo "✅ Docker configuré pour GCR"
echo ""

# 5. Build et push l'image
echo "🏗️  5/7 - Build et push de l'image Docker..."
docker build -t ${IMAGE_NAME}:latest .
docker push ${IMAGE_NAME}:latest
echo "✅ Image pushée: ${IMAGE_NAME}:latest"
echo ""

# 6. Déployer sur Cloud Run
echo "🚀 6/7 - Déploiement sur Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME}:latest \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0 \
  --port 8080 \
  --set-env-vars="MODEL_URI=models:/google-playstore-success-predictor/Production" \
  --set-env-vars="MLFLOW_TRACKING_URI=YOUR_MLFLOW_URI"

echo "✅ Déployé sur Cloud Run"
echo ""

# 7. Récupérer l'URL du service
echo "🌐 7/7 - Récupération de l'URL..."
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --format 'value(status.url)')

echo ""
echo "======================================"
echo "✅ DÉPLOIEMENT RÉUSSI!"
echo "======================================"
echo ""
echo "🌐 URL de l'API:"
echo "   ${SERVICE_URL}"
echo ""
echo "📝 Endpoints disponibles:"
echo "   • Health: ${SERVICE_URL}/health"
echo "   • Info:   ${SERVICE_URL}/info"
echo "   • Predict: ${SERVICE_URL}/predict (POST)"
echo ""
echo "🧪 Test rapide:"
echo "   curl ${SERVICE_URL}/health"
echo ""
echo "💰 Coûts estimés:"
echo "   • Free tier: 2M requêtes/mois"
echo "   • Ensuite: ~0.40$/million requêtes"
echo ""
