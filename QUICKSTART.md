# 🚀 Quick Start - Pipeline MLOps

Guide rapide pour démarrer le pipeline en 5 minutes!

## ⚡ Démarrage Rapide

### 1. Installation (2 minutes)

```bash
# Cloner ou se placer dans le projet
cd mlops-jupyter

# Installer les dépendances
pip install -r requirements.txt

# Vérifier l'installation
python --version  # Devrait être >= 3.8
mlflow --version
```

### 2. Test Local (3 minutes)

```bash
# Lancer le test complet
./test_pipeline.sh

# Ou étape par étape:

# Démarrer MLflow
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlflow/artifacts \
  --host 0.0.0.0 \
  --port 5000 &

# Tester le pipeline
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/check_new_data.py
python src/train_pipeline.py
python src/deployment_decision.py
python src/deploy.py --environment production
```

### 3. Push vers GitHub

```bash
# Créer le repo sur GitHub (via l'interface web)
# Puis:

git init
git add .
git commit -m "Initial commit: MLOps pipeline"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/mlops-jupyter.git
git push -u origin main
```

### 4. Activer GitHub Actions

1. Aller sur GitHub → Votre repo
2. Cliquer sur l'onglet **Actions**
3. Cliquer sur **"I understand my workflows, go ahead and enable them"**
4. Le workflow `ml-pipeline.yml` est maintenant actif! 🎉

### 5. Déclencher le Pipeline

**Option A: Automatique** (quand vous ajoutez des données)
```bash
# Ajouter des données
echo "new_data" >> data/googleplaystore_clean.csv

# Commit et push
git add data/
git commit -m "feat: ajout de nouvelles applications"
git push origin main

# → Pipeline se déclenche automatiquement!
```

**Option B: Manuel** (via GitHub UI)
1. Aller dans **Actions**
2. Sélectionner **ML Pipeline**
3. Cliquer sur **Run workflow**
4. Choisir la branche `main`
5. Cliquer sur **Run workflow**

## 📊 Voir les Résultats

### GitHub Actions
- **URL**: `https://github.com/VOTRE-USERNAME/mlops-jupyter/actions`
- Voir les logs en temps réel
- Télécharger les artifacts (modèles, rapports)

### MLflow UI
```bash
# En local
mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000

# Ouvrir: http://localhost:5000
```

### Fichiers Générés
```
models/
├── candidate_model.pkl          # Nouveau modèle
├── production_model.pkl         # Modèle en production
└── production_model_backup_*.pkl # Backups

reports/
└── report_*.json                # Rapports de performance

logs/
└── deployment.log               # Historique des déploiements
```

## 🔄 Workflow Quotidien

```bash
# 1. Matin: Ajouter des nouvelles données
cat new_apps.csv >> data/googleplaystore_clean.csv

# 2. Commit
git add data/
git commit -m "feat: données du $(date +%Y-%m-%d)"
git push

# 3. GitHub Actions se déclenche
# → Vérifie les données
# → Entraîne si nécessaire
# → Déploie automatiquement si amélioration

# 4. Vérifier les résultats
# → GitHub Actions (logs)
# → MLflow UI (métriques)
# → Notifications (Slack/Email)
```

## 🛠️ Commandes Utiles

```bash
# Tester le pipeline complet
./test_pipeline.sh

# Forcer un réentraînement
python src/train_pipeline.py

# Déployer manuellement
python src/deploy.py --environment production

# Rollback
python src/deploy.py --rollback

# Voir les logs
cat logs/deployment.log

# Nettoyer
rm -rf mlflow/artifacts/*
rm models/*.pkl
```

## 🐛 Dépannage

### Problème: MLflow ne démarre pas
```bash
# Vérifier le port
lsof -i :5000
# ou
netstat -tuln | grep 5000

# Tuer le processus
kill -9 <PID>

# Redémarrer
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000
```

### Problème: GitHub Actions échoue
```bash
# Vérifier les logs dans GitHub
# Actions → Votre workflow → Logs détaillés

# Tester localement d'abord
./test_pipeline.sh
```

### Problème: Pas de nouvelles données détectées
```bash
# Vérifier le seuil (100 apps par défaut)
# Modifier dans src/check_new_data.py:
threshold = 50  # Au lieu de 100

# Ou forcer le réentraînement
python src/train_pipeline.py
```

## 📚 Documentation Complète

Voir [README_PIPELINE.md](README_PIPELINE.md) pour:
- Architecture détaillée
- Configuration avancée
- Monitoring et alertes
- Best practices

## 🎓 Prochaines Étapes

1. **Configurer les notifications**
   - Slack webhook dans `src/notify.py`
   - Email SMTP

2. **Monitoring avancé**
   - Prometheus
   - Grafana
   - Evidently AI (data drift)

3. **Tests plus robustes**
   - Unit tests
   - Integration tests
   - A/B testing

4. **Déploiement cloud**
   - AWS SageMaker
   - Azure ML
   - Google Cloud AI Platform

## 💬 Support

Des questions? Créez une issue sur GitHub!

---

**Happy ML Engineering! 🚀**
