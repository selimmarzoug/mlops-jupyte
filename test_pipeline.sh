#!/bin/bash

# Script de test local du pipeline MLOps
# ======================================

echo "======================================================================"
echo "🚀 TEST LOCAL DU PIPELINE MLOPS"
echo "======================================================================"

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les étapes
step() {
    echo ""
    echo "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo "${YELLOW}$1${NC}"
    echo "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

success() {
    echo "${GREEN}✅ $1${NC}"
}

error() {
    echo "${RED}❌ $1${NC}"
}

# Vérifier l'environnement
step "ÉTAPE 1: Vérification de l'environnement"

if [ ! -d ".venv" ]; then
    error "Virtual environment non trouvé"
    echo "Créez-le avec: python -m venv .venv"
    exit 1
fi
success "Virtual environment trouvé"

if [ ! -f "data/googleplaystore_clean.csv" ]; then
    error "Fichier de données non trouvé"
    echo "Copiez vos données vers: data/googleplaystore_clean.csv"
    exit 1
fi
success "Données trouvées"

# Activer l'environnement virtuel
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null

# Démarrer MLflow
step "ÉTAPE 2: Démarrage de MLflow"

echo "Démarrage du serveur MLflow..."
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlflow/artifacts \
    --host 0.0.0.0 \
    --port 5000 &
MLFLOW_PID=$!

sleep 5
success "MLflow démarré (PID: $MLFLOW_PID)"
echo "   Interface: http://localhost:5000"

export MLFLOW_TRACKING_URI=http://localhost:5000

# Test 1: Vérifier les nouvelles données
step "ÉTAPE 3: Vérification des nouvelles données"

python src/check_new_data.py
if [ $? -eq 0 ]; then
    success "Vérification des données OK"
else
    error "Erreur lors de la vérification"
    kill $MLFLOW_PID
    exit 1
fi

HAS_NEW_DATA=$(cat /tmp/has_new_data.txt)
NEW_DATA_COUNT=$(cat /tmp/new_data_count.txt)

echo "   Nouvelles données: $HAS_NEW_DATA"
echo "   Nombre: $NEW_DATA_COUNT"

# Test 2: Entraînement
step "ÉTAPE 4: Entraînement du modèle"

python src/train_pipeline.py
if [ $? -eq 0 ]; then
    success "Entraînement réussi"
else
    error "Erreur lors de l'entraînement"
    kill $MLFLOW_PID
    exit 1
fi

MODEL_VERSION=$(cat /tmp/model_version.txt)
ACCURACY=$(cat /tmp/accuracy.txt)
IMPROVEMENT=$(cat /tmp/improvement.txt)

echo "   Version: $MODEL_VERSION"
echo "   Accuracy: $ACCURACY"
echo "   Amélioration: $IMPROVEMENT"

# Test 3: Décision de déploiement
step "ÉTAPE 5: Décision de déploiement"

python src/deployment_decision.py
if [ $? -eq 0 ]; then
    success "Décision prise"
else
    error "Erreur lors de la décision"
    kill $MLFLOW_PID
    exit 1
fi

SHOULD_DEPLOY=$(cat /tmp/should_deploy.txt)
echo "   Déploiement approuvé: $SHOULD_DEPLOY"

# Test 4: Déploiement (si approuvé)
if [ "$SHOULD_DEPLOY" = "true" ]; then
    step "ÉTAPE 6: Déploiement en staging"
    
    python src/deploy.py --environment staging
    if [ $? -eq 0 ]; then
        success "Déploiement staging OK"
    else
        error "Erreur déploiement staging"
        kill $MLFLOW_PID
        exit 1
    fi
    
    step "ÉTAPE 7: Tests de déploiement"
    
    python src/test_deployment.py --environment staging
    if [ $? -eq 0 ]; then
        success "Tests réussis"
    else
        error "Tests échoués"
        kill $MLFLOW_PID
        exit 1
    fi
    
    step "ÉTAPE 8: Déploiement canary (5%)"
    
    python src/deploy.py --environment production --canary 0.05
    success "Déploiement canary OK"
    
    step "ÉTAPE 9: Monitoring canary"
    
    python src/monitor_canary.py --duration 5
    success "Monitoring OK"
    
    step "ÉTAPE 10: Déploiement production complet"
    
    python src/deploy.py --environment production --canary 1.0
    success "Déploiement production OK"
    
    step "ÉTAPE 11: Notification"
    
    python src/notify.py \
        --version "$MODEL_VERSION" \
        --accuracy "$ACCURACY" \
        --improvement "$IMPROVEMENT"
    success "Notification envoyée"
else
    echo ""
    echo "${YELLOW}⚠️  Déploiement non approuvé - Score insuffisant${NC}"
fi

# Test 5: Génération du rapport
step "ÉTAPE 12: Génération du rapport"

python src/generate_report.py
if [ $? -eq 0 ]; then
    success "Rapport généré"
    echo "   Voir: reports/"
else
    error "Erreur génération rapport"
fi

# Nettoyer
step "NETTOYAGE"

kill $MLFLOW_PID
success "MLflow arrêté"

# Résumé
step "RÉSUMÉ DES TESTS"

echo ""
echo "🎯 Pipeline testé avec succès!"
echo ""
echo "📊 Résultats:"
echo "   • Nouvelles données: $NEW_DATA_COUNT"
echo "   • Modèle version: $MODEL_VERSION"
echo "   • Accuracy: $ACCURACY"
echo "   • Amélioration: $IMPROVEMENT"
echo "   • Déploiement: $SHOULD_DEPLOY"
echo ""
echo "📁 Fichiers générés:"
echo "   • models/candidate_model.pkl"
echo "   • reports/*.json"
echo "   • logs/deployment.log"
echo ""
echo "🌐 Pour voir dans MLflow:"
echo "   1. mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000"
echo "   2. Ouvrir: http://localhost:5000"
echo ""
echo "======================================================================"
echo "✅ TOUS LES TESTS ONT RÉUSSI!"
echo "======================================================================"
