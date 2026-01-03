"""
Pipeline d'Entraînement avec MLflow
===================================
Entraîne un nouveau modèle et le compare avec le modèle en production
"""

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
import joblib
import os
from datetime import datetime

# Configuration MLflow
MLFLOW_TRACKING_URI = os.environ.get('MLFLOW_TRACKING_URI', 'http://localhost:5000')
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def load_data():
    """Charge et prépare les données"""
    print("📊 Chargement des données...")
    df = pd.read_csv('data/googleplaystore_clean.csv')
    
    # Ici, ajoutez votre logique de preprocessing
    # Pour la démo, on crée des features synthétiques
    X = df.select_dtypes(include=[np.number]).fillna(0)
    
    # Créer une target si elle n'existe pas (exemple)
    if 'Rating' in df.columns:
        y = (df['Rating'] > 4.0).astype(int)
    else:
        # Fallback: target synthétique
        y = (X.iloc[:, 0] > X.iloc[:, 0].median()).astype(int)
    
    print(f"✅ Données chargées: {len(df)} applications")
    print(f"   Features: {X.shape[1]}")
    print(f"   Distribution: {np.mean(y):.1%} succès")
    
    return X, y

def train_model(X_train, y_train, X_test, y_test, experiment_name="google-playstore-ci-cd"):
    """Entraîne plusieurs modèles et sélectionne le meilleur"""
    
    mlflow.set_experiment(experiment_name)
    
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42)
    }
    
    best_model = None
    best_accuracy = 0
    best_metrics = {}
    
    print("\n🔧 Entraînement des modèles...")
    
    for model_name, model in models.items():
        with mlflow.start_run(run_name=f"{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            # Entraînement
            model.fit(X_train, y_train)
            
            # Prédictions
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
            
            # Métriques
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_proba)
            
            # Log dans MLflow
            mlflow.log_param("model_type", model_name)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("roc_auc", roc_auc)
            
            # Log du modèle
            mlflow.sklearn.log_model(model, "model")
            
            print(f"\n{model_name}:")
            print(f"   Accuracy: {accuracy:.4f}")
            print(f"   F1-Score: {f1:.4f}")
            print(f"   ROC-AUC: {roc_auc:.4f}")
            
            # Garder le meilleur
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model
                best_metrics = {
                    'accuracy': accuracy,
                    'f1_score': f1,
                    'roc_auc': roc_auc,
                    'model_name': model_name
                }
    
    return best_model, best_metrics

def compare_with_production(new_metrics):
    """Compare le nouveau modèle avec celui en production"""
    
    print("\n⚖️  Comparaison avec le modèle en production...")
    
    prod_model_path = 'models/production_model.pkl'
    prod_metrics_path = 'models/production_metrics.txt'
    
    if not os.path.exists(prod_metrics_path):
        print("🆕 Pas de modèle en production - premier déploiement")
        improvement = new_metrics['accuracy']
    else:
        with open(prod_metrics_path, 'r') as f:
            prod_accuracy = float(f.read().strip())
        
        improvement = new_metrics['accuracy'] - prod_accuracy
        
        print(f"Production: {prod_accuracy:.4f}")
        print(f"Nouveau:    {new_metrics['accuracy']:.4f}")
        print(f"Différence: {improvement:+.4f} ({(improvement/prod_accuracy)*100:+.2f}%)")
    
    return improvement

def main():
    """Pipeline principal"""
    
    print("="*60)
    print("🚀 PIPELINE D'ENTRAÎNEMENT ML")
    print("="*60)
    
    # Charger les données
    X, y = load_data()
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Entraîner
    best_model, best_metrics = train_model(X_train, y_train, X_test, y_test)
    
    # Comparer
    improvement = compare_with_production(best_metrics)
    
    # Sauvegarder le modèle
    os.makedirs('models', exist_ok=True)
    model_path = 'models/candidate_model.pkl'
    joblib.dump(best_model, model_path)
    
    # Sauvegarder les métriques
    with open('/tmp/model_version.txt', 'w') as f:
        f.write(f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    with open('/tmp/accuracy.txt', 'w') as f:
        f.write(f"{best_metrics['accuracy']:.4f}")
    
    with open('/tmp/improvement.txt', 'w') as f:
        f.write(f"{improvement:.4f}")
    
    # Mettre à jour le compteur de données
    df = pd.read_csv('data/googleplaystore_clean.csv')
    with open('models/last_training_date.txt', 'w') as f:
        f.write(str(len(df)))
    
    print("\n✅ Entraînement terminé avec succès!")
    print(f"📦 Modèle sauvegardé: {model_path}")
    print("="*60)

if __name__ == '__main__':
    main()
