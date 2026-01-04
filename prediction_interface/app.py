#!/usr/bin/env python3
"""
Interface de Prédiction d'Applications
Permet d'ajouter une application et prédire son succès
Utilise le modèle entraîné par le pipeline MLOps
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import mlflow
import os
from datetime import datetime
import logging
import json

app = Flask(__name__)

# Configuration
# Support both local dev (../models) and Docker deployment (./models)
if os.path.exists(os.path.join(os.path.dirname(__file__), 'models')):
    MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
else:
    MODELS_DIR = os.path.join(os.path.dirname(__file__), '../models')

MODEL_FILE = os.path.join(MODELS_DIR, 'model.pkl')
CANDIDATE_MODEL_FILE = os.path.join(MODELS_DIR, 'candidate_model.pkl')
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/googleplaystore_clean.csv')
LOG_FILE = os.path.join(os.path.dirname(__file__), '../logs/predictions.log')
MLFLOW_TRACKING_URI = os.environ.get('MLFLOW_TRACKING_URI', 'http://localhost:5000')

# Logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True) if os.path.dirname(LOG_FILE) else None
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE) if os.path.dirname(LOG_FILE) else logging.NullHandler(),
        logging.StreamHandler()  # Also log to console
    ]
)
logger = logging.getLogger(__name__)

# Variable globale pour le modèle
model = None
model_info = {}

def load_model():
    """Charge le modèle de production ou le dernier modèle entraîné"""
    global model, model_info
    
    try:
        # En production (Cloud Run), charger directement depuis le fichier local
        # Évite le timeout MLflow
        if os.path.exists(MODEL_FILE):
            model = joblib.load(MODEL_FILE)
            model_info = {
                'source': 'Local file',
                'path': MODEL_FILE,
                'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            logger.info(f"✅ Modèle chargé depuis fichier: {MODEL_FILE}")
            return True
        elif os.path.exists(CANDIDATE_MODEL_FILE):
            model = joblib.load(CANDIDATE_MODEL_FILE)
            model_info = {
                'source': 'Candidate model',
                'path': CANDIDATE_MODEL_FILE,
                'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            logger.info(f"✅ Modèle candidat chargé: {CANDIDATE_MODEL_FILE}")
            return True
        else:
            logger.error("❌ Aucun modèle trouvé")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erreur chargement modèle: {e}")
        return False

# Load model at module initialization (for gunicorn)
print("🔄 Initializing model...")
print(f"📂 Looking for model in: {MODELS_DIR}")
print(f"📄 Model file path: {MODEL_FILE}")
print(f"📁 Model file exists: {os.path.exists(MODEL_FILE)}")
if load_model():
    print(f"✅ Model loaded successfully: {model_info.get('source')}")
else:
    print("⚠️  Warning: No model loaded at startup")

def get_categories():
    """Récupère les catégories disponibles depuis les données"""
    try:
        df = pd.read_csv(DATA_FILE)
        categories = sorted(df['Category'].unique().tolist())
        return categories
    except Exception as e:
        logger.error(f"Erreur lecture catégories: {e}")
        return []

def preprocess_input(data):
    """
    Prétraite les données d'entrée pour correspondre au format du modèle
    Le modèle a été entraîné avec Rating et Reviews uniquement
    """
    try:
        # Le modèle utilise uniquement les colonnes numériques du CSV
        # Rating (float) et Reviews (int)
        
        df = pd.DataFrame({
            'Rating': [float(data.get('Rating', 0))],
            'Reviews': [float(data.get('Reviews', 0))]
        })
        
        logger.info(f"Features utilisées: {df.columns.tolist()}")
        logger.info(f"Valeurs: Rating={df['Rating'].values[0]}, Reviews={df['Reviews'].values[0]}")
        
        return df
        
    except Exception as e:
        logger.error(f"Erreur prétraitement: {e}", exc_info=True)
        raise

@app.route('/')
def index():
    """Page d'accueil avec formulaire de prédiction"""
    categories = get_categories()
    
    # Statistiques du modèle
    stats = {
        'model_loaded': model is not None,
        'model_info': model_info,
        'total_categories': len(categories)
    }
    
    return render_template('prediction.html', 
                         categories=categories,
                         stats=stats)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint de prédiction
    Reçoit les données d'une application et retourne la prédiction
    """
    try:
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Modèle non chargé. Veuillez entraîner un modèle d\'abord.'
            }), 503
        
        # Récupérer les données (JSON ou form)
        if request.is_json:
            data = request.get_json()
            app_data = {
                'App': data.get('app_name', 'Test App'),
                'Category': data.get('category', 'LIFESTYLE'),
                'Rating': float(data.get('rating', 0)),
                'Reviews': float(data.get('reviews', 0)),
                'Size': float(data.get('size', 0)),
                'Installs': float(data.get('installs', 0)),
                'Type': 'Free' if float(data.get('price', 0)) == 0 else 'Paid',
                'Price': float(data.get('price', 0)),
                'Content_Rating': data.get('content_rating', 'Everyone')
            }
        else:
            app_data = {
                'App': request.form.get('app_name'),
                'Category': request.form.get('category'),
                'Rating': float(request.form.get('rating', 0)),
                'Reviews': float(request.form.get('reviews', 0)),
                'Size': float(request.form.get('size', 0)),
                'Installs': float(request.form.get('installs', 0)),
                'Type': request.form.get('type', 'Free'),
                'Price': float(request.form.get('price', 0)),
                'Content_Rating': request.form.get('content_rating', 'Everyone')
            }
        
        # Prétraiter les données
        X = preprocess_input(app_data)
        
        # Faire la prédiction
        prediction = model.predict(X)[0]
        
        # Essayer d'obtenir la probabilité si disponible
        confidence = 75.0  # Valeur par défaut
        try:
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X)[0]
                confidence = float(max(proba) * 100)
                logger.info(f"Probabilités: {proba}, Confidence: {confidence}")
            else:
                logger.info("Le modèle n'a pas de predict_proba, utilise confidence par défaut")
        except Exception as e:
            logger.warning(f"Impossible d'obtenir predict_proba: {e}")
            confidence = 75.0
        
        # Interpréter la prédiction
        success = bool(prediction == 1)
        result_text = "Success" if success else "Failure"
        
        # Logger la prédiction
        logger.info(f"Prédiction: {app_data['App']} -> {result_text} (confiance: {confidence:.1f}%) | Rating={app_data['Rating']}, Reviews={app_data['Reviews']}")
        
        # Skip MLflow logging in production for better performance
        # MLflow logging can be enabled in development environment
        
        return jsonify({
            'success': True,
            'prediction': result_text,
            'confidence': round(confidence, 2),
            'app_name': app_data.get('App', 'Test App'),
            'details': {
                'rating': app_data['Rating'],
                'reviews': app_data['Reviews'],
                'installs': app_data['Installs'],
                'size': app_data['Size'],
                'price': app_data['Price']
            }
        })
        
    except Exception as e:
        logger.error(f"Erreur prédiction: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status')
def status():
    """Status de l'API et du modèle"""
    return jsonify({
        'status': 'running',
        'model_loaded': model is not None,
        'model_info': model_info,
        'mlflow_uri': MLFLOW_TRACKING_URI,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/reload_model', methods=['POST'])
def reload_model():
    """Recharge le modèle (utile après un nouvel entraînement)"""
    try:
        success = load_model()
        if success:
            return jsonify({
                'success': True,
                'message': 'Modèle rechargé avec succès',
                'model_info': model_info
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Échec du rechargement du modèle'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Démarrage de l'interface de prédiction...")
    print(f"📊 MLflow URI: {MLFLOW_TRACKING_URI}")
    
    # Charger le modèle au démarrage
    success = load_model()
    if success:
        print(f"✅ Modèle chargé: {model_info.get('source')}")
    else:
        print("⚠️  Aucun modèle chargé - entraînez un modèle d'abord")
    
    print("🌐 Démarrage du serveur sur http://localhost:5003")
    # Démarrer l'application
    app.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)
