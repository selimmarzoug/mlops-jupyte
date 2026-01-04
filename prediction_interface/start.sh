#!/bin/bash
# Script pour démarrer l'interface de prédiction

echo "🚀 Démarrage de l'Interface de Prédiction..."

# Créer les dossiers nécessaires
mkdir -p logs

# Vérifier si le port 5003 est déjà utilisé
if lsof -Pi :5003 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 5003 déjà utilisé. Arrêt du processus..."
    kill $(lsof -t -i:5003) 2>/dev/null
    sleep 2
fi

# Définir l'URI MLflow
export MLFLOW_TRACKING_URI=http://localhost:5000

# Démarrer l'application en arrière-plan
nohup python3 app.py > ../logs/prediction_interface.log 2>&1 &

echo "⏳ Attente du démarrage (3s)..."
sleep 3

# Vérifier si le service est actif
if lsof -Pi :5003 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✅ Interface de Prédiction démarrée sur http://localhost:5003"
    echo "📝 Logs: logs/prediction_interface.log"
else
    echo "❌ Échec du démarrage"
    echo "Vérifiez les logs: logs/prediction_interface.log"
    exit 1
fi
