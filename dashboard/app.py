#!/usr/bin/env python3
"""
Dashboard Automatique des Résultats MLOps
Affiche le meilleur modèle déployé et ses métriques
"""

from flask import Flask, render_template, jsonify
import json
import os
import pickle
from datetime import datetime
import pandas as pd

app = Flask(__name__)

def get_model_info():
    """Récupère les informations du modèle en production"""
    model_path = '../models/production_model.pkl'
    metrics_path = '../models/production_metrics.json'
    
    info = {
        'deployed': False,
        'model_type': 'N/A',
        'size': 'N/A',
        'deployed_at': 'N/A',
        'metrics': {}
    }
    
    # Charger le modèle
    if os.path.exists(model_path):
        info['deployed'] = True
        info['size'] = f"{os.path.getsize(model_path) / 1024:.1f} KB"
        info['deployed_at'] = datetime.fromtimestamp(os.path.getmtime(model_path)).strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            info['model_type'] = type(model).__name__
            
            # Paramètres du modèle
            if hasattr(model, 'n_estimators'):
                info['n_estimators'] = model.n_estimators
            if hasattr(model, 'max_depth'):
                info['max_depth'] = model.max_depth
            if hasattr(model, 'n_features_in_'):
                info['n_features'] = model.n_features_in_
        except Exception as e:
            print(f"Erreur lecture modèle: {e}")
    
    # Charger les métriques
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, 'r') as f:
                info['metrics'] = json.load(f)
        except Exception as e:
            print(f"Erreur lecture métriques: {e}")
    
    return info

def get_deployment_history():
    """Récupère l'historique des déploiements"""
    log_path = '../logs/deployment.log'
    history = []
    
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            lines = f.readlines()
            for line in lines[-20:]:  # 20 dernières lignes
                if line.strip():
                    history.append(line.strip())
    
    return history

def get_data_stats():
    """Récupère les statistiques des données"""
    data_path = '../data/googleplaystore_clean.csv'
    
    stats = {
        'total_apps': 0,
        'categories': 0,
        'last_updated': 'N/A'
    }
    
    if os.path.exists(data_path):
        try:
            df = pd.read_csv(data_path)
            stats['total_apps'] = len(df)
            if 'Category' in df.columns:
                stats['categories'] = df['Category'].nunique()
            stats['last_updated'] = datetime.fromtimestamp(os.path.getmtime(data_path)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Erreur lecture données: {e}")
    
    return stats

def compare_models():
    """Compare le modèle actuel avec le candidat"""
    production_path = '../models/production_model.pkl'
    candidate_path = '../models/candidate_model.pkl'
    production_metrics_path = '../models/production_metrics.json'
    candidate_metrics_path = '../models/candidate_metrics.json'
    
    comparison = {
        'has_both': False,
        'production': {},
        'candidate': {},
        'winner': None
    }
    
    # Métriques production
    if os.path.exists(production_metrics_path):
        with open(production_metrics_path, 'r') as f:
            comparison['production'] = json.load(f)
    
    # Métriques candidat
    if os.path.exists(candidate_metrics_path):
        with open(candidate_metrics_path, 'r') as f:
            comparison['candidate'] = json.load(f)
        comparison['has_both'] = True
    
    # Déterminer le gagnant
    if comparison['has_both']:
        prod_acc = comparison['production'].get('accuracy', 0)
        cand_acc = comparison['candidate'].get('accuracy', 0)
        comparison['winner'] = 'candidate' if cand_acc > prod_acc else 'production'
    
    return comparison

@app.route('/')
def dashboard():
    """Page principale du dashboard"""
    model_info = get_model_info()
    data_stats = get_data_stats()
    comparison = compare_models()
    
    return render_template('dashboard.html', 
                         model=model_info, 
                         data=data_stats,
                         comparison=comparison)

@app.route('/api/model')
def api_model():
    """API: Informations du modèle"""
    return jsonify(get_model_info())

@app.route('/api/history')
def api_history():
    """API: Historique des déploiements"""
    return jsonify({'history': get_deployment_history()})

@app.route('/api/stats')
def api_stats():
    """API: Statistiques des données"""
    return jsonify(get_data_stats())

@app.route('/api/comparison')
def api_comparison():
    """API: Comparaison des modèles"""
    return jsonify(compare_models())

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    print("=" * 80)
    print("🎯 DASHBOARD MLOPS - RÉSULTATS DU MEILLEUR MODÈLE")
    print("=" * 80)
    print()
    print("🌐 Dashboard: http://localhost:5002")
    print("📊 API Model: http://localhost:5002/api/model")
    print("📈 API Stats: http://localhost:5002/api/stats")
    print("🔄 API Comparison: http://localhost:5002/api/comparison")
    print()
    print("Ctrl+C pour arrêter")
    print("=" * 80)
    print()
    
    app.run(host='0.0.0.0', port=5002, debug=True)
