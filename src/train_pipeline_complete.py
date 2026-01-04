"""
Pipeline ML Complet avec Docker et Déploiement Automatique
===========================================================
1. Entraînement de plusieurs modèles
2. Comparaison et sélection du meilleur
3. Déploiement automatique vers l'interface de prédiction
4. Préparation pour Google Cloud
"""

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
import joblib
import os
import json
from datetime import datetime
import shutil

# Configuration MLflow
MLFLOW_TRACKING_URI = os.environ.get('MLFLOW_TRACKING_URI', 'http://localhost:5000')
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def load_data():
    """Charge et prépare les données"""
    print("📊 Chargement des données...")
    df = pd.read_csv('data/googleplaystore_clean.csv')
    
    # Sélectionner uniquement les colonnes numériques
    X = df.select_dtypes(include=[np.number]).fillna(0)
    
    # Créer la target (Rating > 4.0 = Succès)
    if 'Rating' in df.columns:
        y = (df['Rating'] > 4.0).astype(int)
    else:
        y = (X.iloc[:, 0] > X.iloc[:, 0].median()).astype(int)
    
    print(f"✅ Données chargées: {len(df)} applications")
    print(f"   Features: {X.columns.tolist()}")
    print(f"   Distribution: {np.mean(y):.1%} succès")
    
    return X, y, df

def train_and_compare_models(X_train, y_train, X_test, y_test, experiment_name="google-playstore-ci-cd"):
    """
    Entraîne plusieurs modèles et sélectionne le meilleur
    """
    try:
        mlflow.set_experiment(experiment_name)
        use_mlflow = True
    except Exception as e:
        print(f"⚠️ MLflow non disponible: {e}")
        print("   Continuation sans MLflow...")
        use_mlflow = False
    
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
        'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5),
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42)
    }
    
    results = []
    best_model = None
    best_score = 0
    best_model_name = None
    
    print("\n🔧 Entraînement et comparaison des modèles...")
    print("="*60)
    
    for model_name, model in models.items():
        print(f"\n📊 {model_name}:")
        
        try:
            if use_mlflow:
                mlflow_context = mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                mlflow_context.__enter__()
            
            # Entraînement
            model.fit(X_train, y_train)
            
            # Prédictions
            y_pred = model.predict(X_test)
            
            # Métriques
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Cross-validation pour plus de robustesse
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            
            # Calculer le score combiné (moyenne de accuracy et CV)
            combined_score = (accuracy + cv_mean) / 2
            
            # Log dans MLflow si disponible
            if use_mlflow:
                try:
                    mlflow.log_param("model_type", model_name)
                    mlflow.log_metric("accuracy", accuracy)
                    mlflow.log_metric("f1_score", f1)
                    mlflow.log_metric("cv_mean", cv_mean)
                    mlflow.log_metric("cv_std", cv_std)
                    mlflow.log_metric("combined_score", combined_score)
                    mlflow.sklearn.log_model(model, "model")
                except Exception as e:
                    print(f"   ⚠️  MLflow logging échoué: {e}")
            
            print(f"   Accuracy:      {accuracy:.4f}")
            print(f"   F1-Score:      {f1:.4f}")
            print(f"   CV Mean:       {cv_mean:.4f} (+/- {cv_std:.4f})")
            print(f"   Combined:      {combined_score:.4f}")
            
            # Stocker les résultats
            results.append({
                'model_name': model_name,
                'model': model,
                'accuracy': accuracy,
                'f1_score': f1,
                'cv_mean': cv_mean,
                'cv_std': cv_std,
                'combined_score': combined_score
            })
            
            # Garder le meilleur
            if combined_score > best_score:
                best_score = combined_score
                best_model = model
                best_model_name = model_name
            
            if use_mlflow:
                mlflow_context.__exit__(None, None, None)
                    
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            if use_mlflow and 'mlflow_context' in locals():
                try:
                    mlflow_context.__exit__(None, None, None)
                except:
                    pass
            continue
    
    print("\n" + "="*60)
    print(f"🏆 MEILLEUR MODÈLE: {best_model_name}")
    print(f"   Score combiné: {best_score:.4f}")
    print("="*60)
    
    return best_model, best_model_name, results

def compare_with_production(new_accuracy):
    """Compare le nouveau modèle avec celui en production"""
    
    print("\n⚖️  Comparaison avec le modèle en production...")
    
    prod_metrics_path = 'models/production_metrics.json'
    
    if not os.path.exists(prod_metrics_path):
        print("🆕 Pas de modèle en production - premier déploiement")
        return True, new_accuracy
    
    try:
        with open(prod_metrics_path, 'r') as f:
            prod_metrics = json.load(f)
        
        prod_accuracy = prod_metrics.get('accuracy', 0)
        improvement = new_accuracy - prod_accuracy
        
        print(f"   Production:  {prod_accuracy:.4f}")
        print(f"   Nouveau:     {new_accuracy:.4f}")
        print(f"   Différence:  {improvement:+.4f} ({(improvement/prod_accuracy)*100:+.2f}%)")
        
        # Déployer si amélioration > 1% ou si nouveau modèle > 0.80
        should_deploy = improvement > 0.01 or new_accuracy > 0.80
        
        if should_deploy:
            print("✅ Déploiement recommandé")
        else:
            print("⚠️  Pas d'amélioration significative")
        
        return should_deploy, improvement
        
    except Exception as e:
        print(f"⚠️  Erreur lecture métriques production: {e}")
        return True, new_accuracy

def deploy_to_prediction_interface(model, model_name, metrics):
    """
    Déploie le modèle vers l'interface de prédiction
    """
    print("\n📦 Déploiement vers l'interface de prédiction...")
    
    os.makedirs('models', exist_ok=True)
    
    # 1. Sauvegarder le nouveau modèle comme candidat
    candidate_path = 'models/candidate_model.pkl'
    joblib.dump(model, candidate_path)
    print(f"   ✅ Candidat sauvegardé: {candidate_path}")
    
    # 2. Sauvegarder les métriques du candidat
    candidate_metrics = {
        'model_name': model_name,
        'accuracy': metrics['accuracy'],
        'f1_score': metrics['f1_score'],
        'cv_mean': metrics['cv_mean'],
        'cv_std': metrics['cv_std'],
        'combined_score': metrics['combined_score'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('models/candidate_metrics.json', 'w') as f:
        json.dump(candidate_metrics, f, indent=2)
    print(f"   ✅ Métriques sauvegardées: models/candidate_metrics.json")
    
    # 3. Comparer avec production
    should_deploy, improvement = compare_with_production(metrics['accuracy'])
    
    if should_deploy:
        # 4. Promouvoir le candidat en production
        production_path = 'models/model.pkl'
        shutil.copy(candidate_path, production_path)
        print(f"   ✅ Modèle déployé en production: {production_path}")
        
        # 5. Mettre à jour les métriques de production
        with open('models/production_metrics.json', 'w') as f:
            json.dump(candidate_metrics, f, indent=2)
        
        # 6. Mettre à jour la date d'entraînement
        with open('models/last_training_date.txt', 'w') as f:
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        print("   ✅ Modèle prêt pour l'interface de prédiction!")
        print("   ℹ️  Rechargez le modèle dans l'interface: http://localhost:5003")
        return True
    else:
        print("   ⚠️  Modèle non déployé (pas d'amélioration suffisante)")
        return False

def prepare_for_gcp_deployment(model, model_name, metrics):
    """
    Prépare les fichiers pour le déploiement sur Google Cloud
    """
    print("\n☁️  Préparation pour Google Cloud Platform...")
    
    gcp_dir = 'deployment_gcp'
    os.makedirs(gcp_dir, exist_ok=True)
    
    # 1. Copier le modèle
    model_path = os.path.join(gcp_dir, 'model.pkl')
    joblib.dump(model, model_path)
    print(f"   ✅ Modèle copié: {model_path}")
    
    # 2. Créer app.py pour GCP
    app_content = f'''"""
Application Flask pour Google Cloud Run
Modèle: {model_name}
"""

import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

PORT = int(os.getenv("PORT", 8080))

# Charger le modèle
logger.info("Loading model...")
try:
    model = joblib.load('model.pkl')
    logger.info("✅ Model loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load model: {{str(e)}}")
    model = None

@app.route("/", methods=["GET"])
def home():
    return jsonify({{
        "service": "Google Play Store Success Predictor",
        "model": "{model_name}",
        "accuracy": {metrics['accuracy']:.4f},
        "status": "running" if model else "error",
        "endpoints": {{
            "health": "/health",
            "predict": "/predict (POST)"
        }}
    }})

@app.route("/health", methods=["GET"])
def health():
    if model:
        return jsonify({{"status": "healthy", "model_loaded": True}}), 200
    else:
        return jsonify({{"status": "unhealthy", "model_loaded": False}}), 503

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not model:
            return jsonify({{"error": "Model not loaded"}}), 503
        
        data = request.get_json()
        
        if not data:
            return jsonify({{"error": "No data provided"}}), 400
        
        # Créer DataFrame avec Rating et Reviews
        df = pd.DataFrame({{
            'Rating': [float(data.get('rating', 0))],
            'Reviews': [float(data.get('reviews', 0))]
        }})
        
        prediction = model.predict(df)[0]
        
        try:
            proba = model.predict_proba(df)[0]
            confidence = float(max(proba) * 100)
        except:
            confidence = 75.0
        
        return jsonify({{
            'success': True,
            'prediction': int(prediction),
            'result': '✅ SUCCÈS' if prediction == 1 else '❌ ÉCHEC',
            'confidence': round(confidence, 2)
        }})
        
    except Exception as e:
        logger.error(f"Prediction error: {{str(e)}}")
        return jsonify({{"error": str(e)}}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
'''
    
    with open(os.path.join(gcp_dir, 'app.py'), 'w') as f:
        f.write(app_content)
    print(f"   ✅ app.py créé pour GCP")
    
    # 3. Créer requirements.txt
    requirements = '''Flask==2.3.3
flask-cors==4.0.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
joblib==1.3.2
gunicorn==21.2.0
'''
    
    with open(os.path.join(gcp_dir, 'requirements.txt'), 'w') as f:
        f.write(requirements)
    print(f"   ✅ requirements.txt créé")
    
    # 4. Créer Dockerfile optimisé
    dockerfile = '''FROM python:3.8-slim

ENV PYTHONUNBUFFERED=True
ENV PORT=8080

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY model.pkl .

EXPOSE 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
'''
    
    with open(os.path.join(gcp_dir, 'Dockerfile'), 'w') as f:
        f.write(dockerfile)
    print(f"   ✅ Dockerfile créé")
    
    # 5. Créer .dockerignore
    dockerignore = '''__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.log
.git
.gitignore
README.md
'''
    
    with open(os.path.join(gcp_dir, '.dockerignore'), 'w') as f:
        f.write(dockerignore)
    
    # 6. Créer script de déploiement
    deploy_script = f'''#!/bin/bash
# Script de déploiement Google Cloud Run

set -e

echo "🚀 Déploiement sur Google Cloud Run"
echo "===================================="

# Configuration
PROJECT_ID="your-project-id"  # À MODIFIER
REGION="europe-west1"
SERVICE_NAME="playstore-predictor"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "📋 Configuration:"
echo "   Project: $PROJECT_ID"
echo "   Region: $REGION"
echo "   Service: $SERVICE_NAME"
echo ""

# Vérifier gcloud
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI non installé"
    echo "   Installer: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# 1. Build l'image Docker
echo "🔨 Build de l'image Docker..."
docker build -t $IMAGE_NAME .

# 2. Push vers Google Container Registry
echo "📤 Push vers GCR..."
docker push $IMAGE_NAME

# 3. Déployer sur Cloud Run
echo "🚀 Déploiement sur Cloud Run..."
gcloud run deploy $SERVICE_NAME \\
    --image $IMAGE_NAME \\
    --platform managed \\
    --region $REGION \\
    --allow-unauthenticated \\
    --memory 512Mi \\
    --cpu 1 \\
    --max-instances 10 \\
    --port 8080

echo ""
echo "✅ Déploiement terminé!"
echo ""
echo "🌐 URL du service:"
gcloud run services describe $SERVICE_NAME --region $REGION --format "value(status.url)"
echo ""
echo "📊 Informations:"
echo "   Modèle: {model_name}"
echo "   Accuracy: {metrics['accuracy']:.4f}"
echo "   Déployé le: $(date)"
'''
    
    deploy_path = os.path.join(gcp_dir, 'deploy.sh')
    with open(deploy_path, 'w') as f:
        f.write(deploy_script)
    os.chmod(deploy_path, 0o755)
    print(f"   ✅ Script de déploiement créé: {deploy_path}")
    
    # 7. Créer README
    readme = f'''# Déploiement Google Cloud Run

## Modèle
- **Nom**: {model_name}
- **Accuracy**: {metrics['accuracy']:.4f}
- **F1-Score**: {metrics['f1_score']:.4f}
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Déploiement Local (Test)

```bash
# Build l'image
docker build -t playstore-predictor .

# Tester localement
docker run -p 8080:8080 playstore-predictor

# Tester l'API
curl http://localhost:8080/health
curl -X POST http://localhost:8080/predict \\
  -H "Content-Type: application/json" \\
  -d '{{"rating": 4.5, "reviews": 10000}}'
```

## Déploiement sur Google Cloud

### Prérequis
1. Compte Google Cloud Platform
2. gcloud CLI installé
3. Projet GCP créé

### Étapes

1. **Configurer gcloud**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Modifier deploy.sh**
Éditer `deploy.sh` et remplacer `YOUR_PROJECT_ID`

3. **Déployer**
```bash
./deploy.sh
```

4. **Tester**
```bash
# L'URL sera affichée après le déploiement
curl https://your-service-url.run.app/health
```

## API Endpoints

- `GET /` - Informations sur le service
- `GET /health` - Health check
- `POST /predict` - Faire une prédiction

### Exemple de prédiction

```bash
curl -X POST https://your-service-url.run.app/predict \\
  -H "Content-Type: application/json" \\
  -d '{{
    "rating": 4.5,
    "reviews": 10000
  }}'
```

Réponse:
```json
{{
  "success": true,
  "prediction": 1,
  "result": "✅ SUCCÈS",
  "confidence": 95.5
}}
```

## Coûts

Google Cloud Run facture uniquement l'utilisation:
- Gratuit jusqu'à 2M requêtes/mois
- ~$0.40 pour 1M requêtes supplémentaires

## Support

Documentation: https://cloud.google.com/run/docs
'''
    
    with open(os.path.join(gcp_dir, 'README.md'), 'w') as f:
        f.write(readme)
    print(f"   ✅ README créé")
    
    print(f"\n✅ Préparation GCP terminée!")
    print(f"   📁 Dossier: {gcp_dir}/")
    print(f"   📝 Modifiez {gcp_dir}/deploy.sh avec votre PROJECT_ID")
    print(f"   🚀 Puis exécutez: cd {gcp_dir} && ./deploy.sh")

def main():
    """Pipeline principal"""
    
    print("="*60)
    print("🚀 PIPELINE ML COMPLET")
    print("   Docker + Comparaison + Déploiement + GCP")
    print("="*60)
    
    # 1. Charger les données
    X, y, df = load_data()
    
    # 2. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n📊 Split train/test:")
    print(f"   Train: {len(X_train)} samples")
    print(f"   Test:  {len(X_test)} samples")
    
    # 3. Entraîner et comparer les modèles
    best_model, best_model_name, results = train_and_compare_models(
        X_train, y_train, X_test, y_test
    )
    
    if best_model is None:
        print("❌ Aucun modèle n'a pu être entraîné")
        return
    
    # 4. Obtenir les métriques du meilleur modèle
    best_result = [r for r in results if r['model_name'] == best_model_name][0]
    
    # 5. Déployer vers l'interface de prédiction
    deployed = deploy_to_prediction_interface(best_model, best_model_name, best_result)
    
    # 6. Préparer pour Google Cloud (toujours, même si pas déployé en production)
    prepare_for_gcp_deployment(best_model, best_model_name, best_result)
    
    # 7. Résumé final
    print("\n" + "="*60)
    print("✅ PIPELINE TERMINÉ AVEC SUCCÈS!")
    print("="*60)
    print(f"\n🏆 Meilleur modèle: {best_model_name}")
    print(f"   Accuracy:  {best_result['accuracy']:.4f}")
    print(f"   F1-Score:  {best_result['f1_score']:.4f}")
    print(f"   CV Mean:   {best_result['cv_mean']:.4f}")
    
    if deployed:
        print(f"\n✅ Modèle déployé en production")
        print(f"   📁 models/model.pkl")
        print(f"   🌐 Interface: http://localhost:5003")
        print(f"   ℹ️  Rechargez le modèle dans l'interface")
    else:
        print(f"\n⚠️  Modèle candidat sauvegardé (non déployé)")
        print(f"   📁 models/candidate_model.pkl")
    
    print(f"\n☁️  Préparation Google Cloud:")
    print(f"   📁 deployment_gcp/")
    print(f"   🚀 Commandes:")
    print(f"      cd deployment_gcp")
    print(f"      # Modifier deploy.sh avec votre PROJECT_ID")
    print(f"      ./deploy.sh")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    main()
