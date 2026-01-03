"""
MLflow Model Serving API for Google Cloud Platform
Serving: google-playstore-success-predictor
"""

import os
import mlflow
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialiser Flask
app = Flask(__name__)
CORS(app)

# Configuration
MODEL_URI = os.getenv("MODEL_URI", "models:/google-playstore-success-predictor/Production")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
PORT = int(os.getenv("PORT", 8080))

# Charger le modèle
logger.info(f"Loading model from: {MODEL_URI}")
try:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    model = mlflow.pyfunc.load_model(MODEL_URI)
    logger.info("✅ Model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load model: {str(e)}")
    model = None

@app.route("/", methods=["GET"])
def home():
    """Page d'accueil"""
    return jsonify({
        "service": "MLflow Model API",
        "model": "google-playstore-success-predictor",
        "version": "1.0.0",
        "status": "running" if model else "error",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "info": "/info"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    if model:
        return jsonify({"status": "healthy", "model_loaded": True}), 200
    else:
        return jsonify({"status": "unhealthy", "model_loaded": False}), 503

@app.route("/info", methods=["GET"])
def info():
    """Informations sur le modèle"""
    return jsonify({
        "model_name": "google-playstore-success-predictor",
        "model_uri": MODEL_URI,
        "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
        "expected_features": [
            "Rating", "Reviews", "Size", "Installs", "Price",
            "Content Rating", "Genres", "Last Updated", "Android Ver"
        ],
        "output": "Success prediction (0 or 1)"
    })

@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint de prédiction
    
    Body (JSON):
    {
        "instances": [
            {"Rating": 4.5, "Reviews": 1000, ...},
            {"Rating": 3.0, "Reviews": 50, ...}
        ]
    }
    """
    try:
        if not model:
            return jsonify({"error": "Model not loaded"}), 503
        
        # Récupérer les données
        data = request.get_json()
        
        if not data or "instances" not in data:
            return jsonify({
                "error": "Invalid input format",
                "expected": {"instances": [{"feature1": "value1", ...}]}
            }), 400
        
        # Convertir en DataFrame
        df = pd.DataFrame(data["instances"])
        
        # Prédiction
        predictions = model.predict(df)
        
        # Retourner les résultats
        return jsonify({
            "predictions": predictions.tolist(),
            "num_predictions": len(predictions)
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info(f"Starting server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
