#!/usr/bin/env python3
"""
Interface Web pour Ajouter des Nouvelles Applications
Permet aux utilisateurs d'ajouter des apps sans modifier le CSV manuellement
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os
from datetime import datetime
import logging

app = Flask(__name__)

# Configuration
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/googleplaystore_clean.csv')
LOG_FILE = os.path.join(os.path.dirname(__file__), '../logs/data_additions.log')

# Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def index():
    """Page d'accueil avec formulaire"""
    # Lire les statistiques actuelles
    try:
        df = pd.read_csv(DATA_FILE)
        stats = {
            'total_apps': len(df),
            'total_categories': df['Category'].nunique() if 'Category' in df.columns else 0,
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        stats = {'total_apps': 0, 'total_categories': 0, 'last_update': 'N/A'}
        logging.error(f"Erreur lecture stats: {e}")
    
    return render_template('index.html', stats=stats)

@app.route('/add_app', methods=['POST'])
def add_app():
    """Ajouter une nouvelle application"""
    try:
        # Récupérer les données du formulaire
        app_data = {
            'App': request.form.get('app_name'),
            'Category': request.form.get('category'),
            'Rating': float(request.form.get('rating', 0)),
            'Reviews': int(request.form.get('reviews', 0)),
            'Size': request.form.get('size', '0'),
            'Installs': request.form.get('installs', '0'),
            'Type': request.form.get('type', 'Free'),
            'Price': request.form.get('price', '0'),
            'Content Rating': request.form.get('content_rating', 'Everyone'),
            'Genres': request.form.get('genres', 'Unknown'),
            'Last Updated': datetime.now().strftime('%B %d, %Y'),
            'Current Ver': request.form.get('current_ver', '1.0'),
            'Android Ver': request.form.get('android_ver', '4.0 and up')
        }
        
        # Validation basique
        if not app_data['App'] or not app_data['Category']:
            return jsonify({
                'success': False,
                'message': 'Le nom et la catégorie sont obligatoires'
            }), 400
        
        # Lire le CSV existant
        df = pd.read_csv(DATA_FILE)
        
        # Vérifier si l'app existe déjà
        if app_data['App'] in df['App'].values:
            return jsonify({
                'success': False,
                'message': f"L'application '{app_data['App']}' existe déjà"
            }), 400
        
        # Ajouter la nouvelle ligne
        new_row = pd.DataFrame([app_data])
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Sauvegarder
        df.to_csv(DATA_FILE, index=False)
        
        # Logger
        logging.info(f"Nouvelle app ajoutée: {app_data['App']} - Catégorie: {app_data['Category']}")
        
        return jsonify({
            'success': True,
            'message': f"Application '{app_data['App']}' ajoutée avec succès!",
            'total_apps': len(df)
        })
        
    except Exception as e:
        logging.error(f"Erreur ajout app: {e}")
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500

@app.route('/bulk_upload', methods=['POST'])
def bulk_upload():
    """Upload en masse via fichier CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'Aucun fichier fourni'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Nom de fichier vide'}), 400
        
        # Lire le CSV uploadé
        new_apps_df = pd.read_csv(file)
        
        # Lire le CSV existant
        existing_df = pd.read_csv(DATA_FILE)
        
        # Fusionner (éviter les doublons)
        combined_df = pd.concat([existing_df, new_apps_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['App'], keep='first')
        
        # Sauvegarder
        combined_df.to_csv(DATA_FILE, index=False)
        
        new_count = len(combined_df) - len(existing_df)
        
        logging.info(f"Upload en masse: {new_count} nouvelles apps ajoutées")
        
        return jsonify({
            'success': True,
            'message': f'{new_count} nouvelles applications ajoutées!',
            'total_apps': len(combined_df)
        })
        
    except Exception as e:
        logging.error(f"Erreur upload en masse: {e}")
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500

@app.route('/stats')
def stats():
    """Retourne les statistiques en JSON"""
    try:
        df = pd.read_csv(DATA_FILE)
        
        stats_data = {
            'total_apps': len(df),
            'categories': df['Category'].value_counts().to_dict() if 'Category' in df.columns else {},
            'avg_rating': float(df['Rating'].mean()) if 'Rating' in df.columns else 0,
            'total_reviews': int(df['Reviews'].sum()) if 'Reviews' in df.columns else 0,
            'free_vs_paid': df['Type'].value_counts().to_dict() if 'Type' in df.columns else {}
        }
        
        return jsonify(stats_data)
        
    except Exception as e:
        logging.error(f"Erreur stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/recent_additions')
def recent_additions():
    """Voir les dernières applications ajoutées"""
    try:
        df = pd.read_csv(DATA_FILE)
        # Les 10 dernières lignes (plus récentes)
        recent = df.tail(10).to_dict('records')
        return jsonify({'recent_apps': recent})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Créer le dossier logs si nécessaire
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    print("🚀 Interface Web Démarrée!")
    print("📝 Accédez à: http://localhost:5001")
    print("📊 Stats: http://localhost:5001/stats")
    print("📋 Récents: http://localhost:5001/recent_additions")
    print("\nCtrl+C pour arrêter")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
