#!/usr/bin/env python3
"""
Crée des fichiers de démo pour tester le dashboard
"""

import json
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Créer le dossier models s'il n'existe pas
os.makedirs('models', exist_ok=True)

# 1. Créer un modèle de démo
print("📦 Création du modèle de démo...")
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

# Entraîner avec des données factices
X_demo = np.random.rand(100, 10)
y_demo = np.random.randint(0, 2, 100)
model.fit(X_demo, y_demo)

# Sauvegarder le modèle
with open('models/production_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Modèle sauvegardé: models/production_model.pkl ({os.path.getsize('models/production_model.pkl') / 1024:.1f} KB)")

# 2. Créer des métriques de démo
print("📊 Création des métriques de démo...")
metrics = {
    'accuracy': 0.875,
    'precision': 0.882,
    'recall': 0.868,
    'f1_score': 0.875,
    'model_type': 'RandomForestClassifier',
    'training_date': '2026-01-03 17:00:00'
}

with open('models/production_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print(f"✅ Métriques sauvegardées: models/production_metrics.json")

# 3. Créer un modèle candidat pour la comparaison
print("🆕 Création du modèle candidat...")
candidate_model = RandomForestClassifier(n_estimators=150, max_depth=15, random_state=43)
candidate_model.fit(X_demo, y_demo)

with open('models/candidate_model.pkl', 'wb') as f:
    pickle.dump(candidate_model, f)

candidate_metrics = {
    'accuracy': 0.892,
    'precision': 0.895,
    'recall': 0.888,
    'f1_score': 0.891,
    'model_type': 'RandomForestClassifier',
    'training_date': '2026-01-03 17:15:00'
}

with open('models/candidate_metrics.json', 'w') as f:
    json.dump(candidate_metrics, f, indent=2)

print(f"✅ Modèle candidat sauvegardé: models/candidate_model.pkl")

print("\n" + "="*60)
print("🎉 Fichiers de démo créés avec succès!")
print("="*60)
print("\nRésumé:")
print(f"  📦 Modèle Production: RandomForest (100 arbres)")
print(f"  📊 Accuracy Production: 87.5%")
print(f"  🆕 Modèle Candidat: RandomForest (150 arbres)")
print(f"  📊 Accuracy Candidat: 89.2%")
print(f"  🏆 Gagnant: Candidat (+1.7%)")
print("\n👉 Relancez le dashboard: ./start_dashboard.sh")
print("   ou rafraîchissez: http://localhost:5002\n")
