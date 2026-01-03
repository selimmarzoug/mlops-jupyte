#!/usr/bin/env python3
"""
Script pour analyser les résultats du déploiement MLOps
"""

import os
import json
import pickle
from datetime import datetime

def analyze_deployment():
    """Analyse le modèle déployé et ses métriques"""
    
    print("=" * 80)
    print("🔍 ANALYSE DU DÉPLOIEMENT MLOPS")
    print("=" * 80)
    print()
    
    # 1. Vérifier les modèles disponibles
    models_dir = "../models"
    print("📦 MODÈLES DISPONIBLES:")
    print("-" * 80)
    
    if os.path.exists(models_dir):
        for file in sorted(os.listdir(models_dir)):
            if file.endswith('.pkl'):
                file_path = os.path.join(models_dir, file)
                size = os.path.getsize(file_path)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                # Charger le modèle pour voir le type
                try:
                    with open(file_path, 'rb') as f:
                        model = pickle.load(f)
                    model_type = type(model).__name__
                    
                    print(f"  ✅ {file}")
                    print(f"     Type: {model_type}")
                    print(f"     Taille: {size / 1024:.1f} KB")
                    print(f"     Modifié: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Si c'est le modèle de production, afficher plus de détails
                    if 'production' in file:
                        print(f"     🚀 MODÈLE EN PRODUCTION")
                        
                        # Essayer d'obtenir les paramètres
                        if hasattr(model, 'n_estimators'):
                            print(f"     Paramètres: n_estimators={model.n_estimators}")
                        if hasattr(model, 'max_depth'):
                            print(f"                 max_depth={model.max_depth}")
                    print()
                    
                except Exception as e:
                    print(f"  ⚠️  {file} (erreur de lecture: {e})")
                    print()
    else:
        print("  ❌ Dossier models/ non trouvé")
    
    print()
    
    # 2. Vérifier les métriques sauvegardées
    metrics_files = [
        "../models/candidate_metrics.json",
        "../models/production_metrics.json",
        "../reports/report_*.json"
    ]
    
    print("📊 MÉTRIQUES DE PERFORMANCE:")
    print("-" * 80)
    
    # Chercher les fichiers de métriques
    candidate_metrics_file = "../models/candidate_metrics.json"
    if os.path.exists(candidate_metrics_file):
        with open(candidate_metrics_file, 'r') as f:
            metrics = json.load(f)
        
        print("  🆕 NOUVEAU MODÈLE (Candidate):")
        print(f"     Accuracy:  {metrics.get('accuracy', 'N/A'):.4f}")
        print(f"     Precision: {metrics.get('precision', 'N/A'):.4f}")
        print(f"     Recall:    {metrics.get('recall', 'N/A'):.4f}")
        print(f"     F1-Score:  {metrics.get('f1_score', 'N/A'):.4f}")
        print()
    
    production_metrics_file = "../models/production_metrics.json"
    if os.path.exists(production_metrics_file):
        with open(production_metrics_file, 'r') as f:
            metrics = json.load(f)
        
        print("  🚀 MODÈLE EN PRODUCTION:")
        print(f"     Accuracy:  {metrics.get('accuracy', 'N/A'):.4f}")
        print(f"     Precision: {metrics.get('precision', 'N/A'):.4f}")
        print(f"     Recall:    {metrics.get('recall', 'N/A'):.4f}")
        print(f"     F1-Score:  {metrics.get('f1_score', 'N/A'):.4f}")
        print()
    
    # 3. Lire les logs de déploiement
    logs_file = "../logs/deployment.log"
    print("📝 HISTORIQUE DE DÉPLOIEMENT:")
    print("-" * 80)
    
    if os.path.exists(logs_file):
        with open(logs_file, 'r') as f:
            lines = f.readlines()
            # Afficher les 10 dernières lignes
            for line in lines[-10:]:
                print(f"  {line.strip()}")
    else:
        print("  ℹ️  Aucun log de déploiement trouvé")
    
    print()
    
    # 4. Résumé de la décision de déploiement
    decision_file = "/tmp/should_deploy.txt"
    print("🎯 DÉCISION DE DÉPLOIEMENT:")
    print("-" * 80)
    
    if os.path.exists(decision_file):
        with open(decision_file, 'r') as f:
            should_deploy = f.read().strip()
        
        if should_deploy.lower() == 'true':
            print("  ✅ DÉPLOIEMENT APPROUVÉ")
            print("  Raison: Le nouveau modèle a obtenu un score suffisant (≥70/100)")
        else:
            print("  ❌ DÉPLOIEMENT REJETÉ")
            print("  Raison: Score insuffisant (<70/100)")
    else:
        print("  ℹ️  Fichier de décision non trouvé")
    
    print()
    
    # 5. Vérifier le nombre d'applications dans les données
    data_file = "../data/googleplaystore_clean.csv"
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            line_count = sum(1 for line in f) - 1  # -1 pour l'en-tête
        
        print("📱 DONNÉES D'ENTRAÎNEMENT:")
        print("-" * 80)
        print(f"  Total d'applications: {line_count:,}")
        print(f"  Seuil de réentraînement: 100 nouvelles apps")
        print()
    
    print("=" * 80)
    print("✅ Analyse terminée!")
    print("=" * 80)

if __name__ == "__main__":
    analyze_deployment()
