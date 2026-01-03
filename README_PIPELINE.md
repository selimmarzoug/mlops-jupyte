# 🚀 Pipeline MLOps - CI/CD avec GitHub Actions et MLflow

Pipeline complet d'entraînement, validation et déploiement automatique de modèles ML.

## 📋 Table des Matières

- [Architecture](#architecture)
- [Setup Initial](#setup-initial)
- [Comment ça marche](#comment-ça-marche)
- [Déclencheurs du Pipeline](#déclencheurs-du-pipeline)
- [Tester en Local](#tester-en-local)
- [Configuration GitHub](#configuration-github)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PIPELINE CI/CD MLOPS                        │
└─────────────────────────────────────────────────────────────────┘

1. DÉTECTION DE NOUVELLES DONNÉES
   ├── Vérifier si nouvelles apps >= 100
   └── Déclencher pipeline si seuil atteint

2. RÉENTRAÎNEMENT
   ├── Charger données (anciennes + nouvelles)
   ├── Entraîner plusieurs modèles (RandomForest, LogReg)
   ├── Sélectionner le meilleur
   └── Logger dans MLflow

3. VALIDATION & COMPARAISON
   ├── Comparer avec modèle en production
   ├── Calculer amélioration
   └── Score de confiance

4. DÉCISION AUTOMATIQUE
   ├── Score >= 70%: ✅ Déploiement auto
   ├── Score 50-70%: 🟡 Validation manuelle
   └── Score < 50%: ❌ Rejet

5. DÉPLOIEMENT PROGRESSIF
   ├── Staging → Tests
   ├── Canary (5% trafic) → Monitoring 5min
   ├── Rollout progressif (25% → 50% → 100%)
   └── Production complète

6. MONITORING
   ├── Métriques en temps réel
   ├── Alertes si dégradation
   └── Rollback automatique si nécessaire
```

## 🚦 Setup Initial

### 1. Cloner et Configurer

```bash
# Cloner le repo
git clone <votre-repo>
cd mlops-jupyter

# Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancer MLflow en Local

```bash
# Démarrer le serveur MLflow
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlflow/artifacts \
  --host 0.0.0.0 \
  --port 5000

# Accéder à l'interface: http://localhost:5000
```

### 3. Préparer les Données

```bash
# Copier vos données
cp your_data.csv data/googleplaystore_clean.csv
```

## 🎯 Comment ça marche

### Déclencheurs Automatiques

Le pipeline se déclenche automatiquement dans 3 cas:

1. **Push sur main** (après merge d'un PR)
   ```bash
   git add .
   git commit -m "Ajout de nouvelles applications"
   git push origin main
   ```

2. **Programmé** (tous les jours à 2h UTC)
   - Automatique via GitHub Actions

3. **Manuel** (via GitHub UI)
   - Aller dans Actions → ML Pipeline → Run workflow

### Workflow Complet

```bash
# Exemple: Ajouter de nouvelles données

# 1. Ajouter des données
echo "new_app_data" >> data/googleplaystore_clean.csv

# 2. Commit et push
git add data/
git commit -m "feat: ajout de 150 nouvelles applications"
git push origin main

# 3. GitHub Actions se déclenche automatiquement:
#    ✅ Détecte 150 nouvelles apps (>= seuil de 100)
#    ✅ Réentraîne les modèles
#    ✅ Compare avec production
#    ✅ Décide du déploiement (score 85/100)
#    ✅ Déploie en staging
#    ✅ Tests automatiques
#    ✅ Déploie en production (canary → full)
#    ✅ Monitoring actif
#    ✅ Notification envoyée

# 4. Vérifier dans GitHub Actions
#    - Voir les logs en temps réel
#    - Télécharger les rapports
#    - Consulter les métriques MLflow
```

## 🧪 Tester en Local

### Test du Pipeline Complet

```bash
# 1. Vérifier les nouvelles données
python src/check_new_data.py

# 2. Entraîner le modèle
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/train_pipeline.py

# 3. Décision de déploiement
python src/deployment_decision.py

# 4. Déployer (si approuvé)
python src/deploy.py --environment staging
python src/test_deployment.py --environment staging
python src/deploy.py --environment production --canary 0.05
python src/monitor_canary.py --duration 300
python src/deploy.py --environment production --canary 1.0

# 5. Notification
python src/notify.py --version v20260103 --accuracy 0.92 --improvement 0.015
```

### Test de Rollback

```bash
# Simuler un problème et rollback
python src/deploy.py --rollback
python src/notify.py --rollback --reason "Performance dégradée"
```

## ⚙️ Configuration GitHub

### 1. Créer le Repository

```bash
# Initialiser Git
git init
git add .
git commit -m "Initial commit: MLOps pipeline"

# Créer le repo sur GitHub (via UI)
# Puis:
git remote add origin https://github.com/votre-username/mlops-jupyter.git
git branch -M main
git push -u origin main
```

### 2. Configuration des Secrets (optionnel)

Dans GitHub → Settings → Secrets → Actions, ajouter:

```yaml
MLFLOW_TRACKING_URI: your-mlflow-server-url
SLACK_WEBHOOK: your-slack-webhook
EMAIL_SMTP: your-smtp-config
```

### 3. Activer GitHub Actions

- Aller dans l'onglet "Actions"
- Le workflow `.github/workflows/ml-pipeline.yml` est automatiquement détecté
- Cliquer sur "I understand, enable them"

## 📊 Monitoring avec MLflow

### Accéder à MLflow UI

```bash
# Local
http://localhost:5000

# Voir les runs
# Comparer les modèles
# Télécharger les artifacts
```

### API MLflow

```python
import mlflow

# Charger un modèle
model = mlflow.sklearn.load_model("models:/production-model/latest")

# Faire une prédiction
predictions = model.predict(X_new)
```

## 🔧 Structure du Projet

```
mlops-jupyter/
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml       # Workflow GitHub Actions
├── src/
│   ├── check_new_data.py         # Détection nouvelles données
│   ├── train_pipeline.py         # Pipeline d'entraînement
│   ├── deployment_decision.py    # Décision auto déploiement
│   ├── deploy.py                 # Script de déploiement
│   ├── test_deployment.py        # Tests smoke
│   ├── monitor_canary.py         # Monitoring canary
│   ├── generate_report.py        # Génération rapports
│   └── notify.py                 # Notifications
├── data/
│   └── googleplaystore_clean.csv # Données
├── models/
│   ├── production_model.pkl      # Modèle en prod
│   ├── candidate_model.pkl       # Modèle candidat
│   └── last_training_date.txt    # Tracking
├── mlflow/
│   └── artifacts/                # Artifacts MLflow
├── logs/
│   └── deployment.log            # Logs déploiement
├── reports/
│   └── report_*.json             # Rapports performance
├── requirements.txt
└── README_PIPELINE.md
```

## 📈 Critères de Déploiement

### Score Automatique (sur 100 points)

| Critère | Points | Condition |
|---------|--------|-----------|
| Amélioration > 1% | 40 | Différence accuracy |
| Amélioration > 0% | 20 | Légère amélioration |
| Accuracy > 90% | 30 | Qualité absolue |
| Accuracy > 80% | 20 | Bonne qualité |
| Stabilité | 30 | Métriques cohérentes |

### Décisions

- **Score ≥ 70**: ✅ Déploiement automatique
- **Score 50-69**: 🟡 Validation manuelle requise
- **Score < 50**: ❌ Déploiement refusé

## 🚨 Rollback Automatique

Le rollback se déclenche automatiquement si:

- Déploiement échoue
- Tests smoke échouent
- Performance baisse > 2% après déploiement
- Erreur système détectée

```bash
# Rollback manuel
python src/deploy.py --rollback
```

## 📧 Notifications

Configurez les notifications dans `src/notify.py`:

- **Slack**: Webhook
- **Email**: SMTP
- **Teams**: Webhook
- **PagerDuty**: API

## 🎓 Workflow Recommandé

### Development

```bash
# 1. Créer une branche
git checkout -b feature/new-model

# 2. Développer
# - Modifier le preprocessing
# - Tester de nouveaux modèles
# - Améliorer les features

# 3. Tester localement
python src/train_pipeline.py

# 4. Commit et push
git add .
git commit -m "feat: nouveau feature engineering"
git push origin feature/new-model

# 5. Créer une Pull Request
# - Review du code
# - Tests automatiques

# 6. Merge vers main
# - Pipeline CI/CD se déclenche automatiquement
```

## 💡 Best Practices

1. **Versionner les modèles** avec MLflow
2. **Tester en staging** avant production
3. **Monitoring continu** post-déploiement
4. **Garder des backups** (5 dernières versions)
5. **Documenter** chaque déploiement
6. **Rollback rapide** en cas de problème

## 🔗 Ressources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Scikit-learn](https://scikit-learn.org/)

## 📝 License

MIT

---

**Créé avec ❤️ pour le MLOps**
