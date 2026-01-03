#!/bin/bash
# Script pour télécharger et analyser les artifacts GitHub Actions

echo "🔍 Analyse des Artifacts GitHub Actions"
echo "========================================"
echo ""

# Vérifier si gh CLI est installé
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI (gh) n'est pas installé"
    echo "Installation: sudo apt install gh"
    echo ""
    echo "En attendant, téléchargez manuellement les artifacts:"
    echo "👉 https://github.com/selimmarzoug/mlops-jupyte/actions"
    echo ""
    exit 1
fi

# Télécharger les artifacts du dernier workflow
echo "📥 Téléchargement des artifacts..."
gh run download -R selimmarzoug/mlops-jupyte

echo ""
echo "✅ Artifacts téléchargés!"
echo ""
echo "📂 Fichiers disponibles:"
ls -lh

echo ""
echo "🔍 Pour voir le modèle déployé:"
echo "   python3 -c \"import pickle; m = pickle.load(open('trained-model', 'rb')); print(type(m).__name__)\""
