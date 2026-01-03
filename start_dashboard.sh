#!/bin/bash
# Script de lancement automatique du dashboard après le pipeline

echo "🚀 Lancement Automatique du Dashboard MLOps"
echo "=========================================="
echo ""

# Vérifier si le dashboard tourne déjà
if lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Dashboard déjà actif sur http://localhost:5002"
    echo ""
    echo "Pour le relancer:"
    echo "  1. Trouver le PID: lsof -i:5002"
    echo "  2. Arrêter: kill -9 <PID>"
    echo "  3. Relancer: ./start_dashboard.sh"
else
    echo "📊 Démarrage du dashboard..."
    cd "$(dirname "$0")/dashboard"
    
    # Lancer en arrière-plan
    nohup python3 app.py > ../logs/dashboard.log 2>&1 &
    
    sleep 2
    
    if lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null ; then
        echo ""
        echo "✅ Dashboard démarré avec succès!"
        echo ""
        echo "🌐 Accès:"
        echo "   Dashboard: http://localhost:5002"
        echo "   API Model: http://localhost:5002/api/model"
        echo "   API Stats: http://localhost:5002/api/stats"
        echo ""
        echo "📝 Logs: logs/dashboard.log"
        echo ""
        echo "Pour arrêter:"
        echo "   kill -9 \$(lsof -t -i:5002)"
    else
        echo "❌ Échec du démarrage"
        echo "Voir les logs: cat logs/dashboard.log"
    fi
fi

echo ""
echo "=========================================="
