#!/usr/bin/env python3
"""
Génère un rapport HTML automatique après le déploiement
"""

import json
import os
import pickle
from datetime import datetime

def generate_html_report():
    """Génère un rapport HTML complet"""
    
    # Charger les métriques
    metrics = {}
    metrics_file = 'models/candidate_metrics.json'
    if os.path.exists(metrics_file):
        with open(metrics_file, 'r') as f:
            metrics = json.load(f)
    
    # Charger info modèle
    model_info = {}
    model_file = 'models/candidate_model.pkl'
    if os.path.exists(model_file):
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
        model_info['type'] = type(model).__name__
        model_info['size'] = f"{os.path.getsize(model_file) / 1024:.1f} KB"
        
        if hasattr(model, 'n_estimators'):
            model_info['n_estimators'] = model.n_estimators
        if hasattr(model, 'max_depth'):
            model_info['max_depth'] = model.max_depth
    
    # Générer le HTML
    html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport MLOps - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #1e3c72;
            text-align: center;
            margin-bottom: 30px;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 15px;
            background: white;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .metric-label {{
            font-weight: bold;
            color: #666;
        }}
        .metric-value {{
            color: #1e3c72;
            font-size: 1.2em;
            font-weight: bold;
        }}
        .good {{ color: #28a745; }}
        .medium {{ color: #ffc107; }}
        .bad {{ color: #dc3545; }}
        .status {{
            text-align: center;
            padding: 20px;
            background: #d4edda;
            color: #155724;
            border-radius: 10px;
            font-size: 1.3em;
            font-weight: bold;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Rapport MLOps - Meilleur Modèle Déployé</h1>
        
        <div class="status">
            ✅ Pipeline Exécuté avec Succès
        </div>
        
        <div class="section">
            <h2>📦 Informations du Modèle</h2>
            <div class="metric">
                <span class="metric-label">Type de Modèle</span>
                <span class="metric-value">{model_info.get('type', 'N/A')}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Taille du Fichier</span>
                <span class="metric-value">{model_info.get('size', 'N/A')}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Date de Création</span>
                <span class="metric-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
            </div>
            {'<div class="metric"><span class="metric-label">Nombre d\'Arbres</span><span class="metric-value">' + str(model_info.get('n_estimators', 'N/A')) + '</span></div>' if 'n_estimators' in model_info else ''}
            {'<div class="metric"><span class="metric-label">Profondeur Max</span><span class="metric-value">' + str(model_info.get('max_depth', 'N/A')) + '</span></div>' if 'max_depth' in model_info else ''}
        </div>
        
        <div class="section">
            <h2>📊 Métriques de Performance</h2>
            <div class="metric">
                <span class="metric-label">Accuracy</span>
                <span class="metric-value {'good' if metrics.get('accuracy', 0) >= 0.85 else 'medium' if metrics.get('accuracy', 0) >= 0.75 else 'bad'}">
                    {metrics.get('accuracy', 0) * 100:.2f}%
                </span>
            </div>
            <div class="metric">
                <span class="metric-label">Precision</span>
                <span class="metric-value">{metrics.get('precision', 0) * 100:.2f}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">Recall</span>
                <span class="metric-value">{metrics.get('recall', 0) * 100:.2f}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">F1-Score</span>
                <span class="metric-value">{metrics.get('f1_score', 0) * 100:.2f}%</span>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Décision de Déploiement</h2>
            <p style="text-align: center; font-size: 1.2em; padding: 20px;">
                Le modèle a été <strong style="color: #28a745;">approuvé pour le déploiement</strong><br>
                Score global: <strong>{metrics.get('accuracy', 0) * 100:.1f}/100</strong>
            </p>
        </div>
        
        <div style="text-align: center; color: #666; margin-top: 40px;">
            <p>Rapport généré automatiquement par le pipeline MLOps</p>
            <p>GitHub Actions • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
    """
    
    # Sauvegarder le rapport
    os.makedirs('reports', exist_ok=True)
    output_file = f'reports/dashboard_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Créer aussi un lien vers le dernier rapport
    latest_file = 'reports/dashboard_report.html'
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Rapport HTML généré: {output_file}")
    print(f"✅ Dernier rapport: {latest_file}")
    
    return output_file

if __name__ == '__main__':
    generate_html_report()
