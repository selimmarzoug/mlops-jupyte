# Interface de Prédiction d'Applications

Interface web pour prédire le succès d'une application Google Play Store basée sur ses caractéristiques.

## 🎯 Fonctionnalités

- **Formulaire intuitif** pour saisir les données d'une application
- **Prédiction en temps réel** utilisant le modèle entraîné par le pipeline MLOps
- **Affichage du niveau de confiance** de la prédiction
- **Intégration MLflow** pour le suivi des prédictions
- **Rechargement du modèle** sans redémarrer le service

## 🚀 Démarrage

```bash
# Démarrer l'interface
./start.sh

# L'interface sera disponible sur:
# http://localhost:5003
```

## 📊 Utilisation

1. **Remplir le formulaire** avec les informations de l'application :
   - Nom de l'application
   - Catégorie
   - Rating (0-5)
   - Nombre de reviews
   - Taille en MB
   - Nombre d'installations
   - Type (Gratuite/Payante)
   - Prix
   - Classification de contenu

2. **Cliquer sur "Prédire le Succès"**

3. **Voir le résultat** :
   - ✅ SUCCÈS : L'application devrait avoir un rating > 4.0
   - ❌ ÉCHEC : L'application risque d'avoir un rating ≤ 4.0
   - Niveau de confiance en pourcentage

## 🔧 Configuration

L'interface charge automatiquement le modèle depuis :
1. **MLflow** (Production) en priorité : `models:/google-playstore-success-predictor/Production`
2. **Fichier local** : `models/model.pkl`
3. **Modèle candidat** : `models/candidate_model.pkl`

## 🔄 Workflow avec le Pipeline

1. **Entraîner un modèle** avec le pipeline :
   ```bash
   python src/train_pipeline.py
   ```

2. **Recharger le modèle** dans l'interface :
   - Cliquer sur le bouton "🔄 Recharger Modèle"
   - Ou redémarrer l'interface

3. **Faire des prédictions** avec le nouveau modèle

## 📝 Logs

Les prédictions sont enregistrées dans :
- `logs/prediction_interface.log` : Logs du serveur
- `logs/predictions.log` : Historique des prédictions
- MLflow (si disponible) : Runs de prédiction

## 🔗 Endpoints API

- `GET /` : Interface web
- `POST /predict` : Faire une prédiction
- `GET /api/status` : Status du service
- `POST /reload_model` : Recharger le modèle

## ⚙️ Variables d'Environnement

- `MLFLOW_TRACKING_URI` : URI du serveur MLflow (défaut: `http://localhost:5000`)
- `PORT` : Port du serveur (défaut: `5003`)

## 🧪 Exemple d'Utilisation via API

```bash
curl -X POST http://localhost:5003/predict \
  -F "app_name=My App" \
  -F "category=GAME" \
  -F "rating=4.5" \
  -F "reviews=1000" \
  -F "size=50" \
  -F "installs=100000" \
  -F "type=Free" \
  -F "price=0" \
  -F "content_rating=Everyone"
```

## 🛑 Arrêter l'Interface

```bash
# Trouver et arrêter le processus
kill $(lsof -t -i:5003)
```
