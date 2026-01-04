# 🚀 GitHub Actions - Pipeline ML Complet

Ce dossier contient le workflow GitHub Actions pour automatiser l'intégralité du pipeline MLOps.

## 📋 Workflow Unifié

### 🎯 ML Pipeline Complete - Train + Docker Build (`docker-build.yml`)

**Un seul workflow qui fait TOUT:**

1. 🤖 **Entraîne les modèles ML** (RandomForest, GradientBoosting, LogisticRegression)
2. 📊 **Compare et sélectionne le meilleur**
3. 💾 **Génère les fichiers** (model.pkl, métriques, déploiement GCP)
4. 🐳 **Construit l'image Docker**
5. 🧪 **Teste l'image Docker**
6. 📤 **Upload les artifacts**

**Déclenchement:**
- Push sur `main` ou `master`
- Modification des fichiers: `src/**`, `data/**`, `Dockerfile.pipeline`, `requirements.txt`
- Manuellement via l'interface GitHub

**Durée:** ~10-15 minutes

## 🎬 Utilisation Manuelle

1. Aller sur GitHub → Actions
2. Sélectionner "ML Pipeline Complete - Train + Docker Build"
3. Cliquer sur "Run workflow"
4. Sélectionner la branche "main"
5. Cliquer "Run workflow"

## 📊 Ce que fait le workflow

```
┌──────────────────────┐
│   ÉTAPE 1: ML        │
│   Entraînement       │ ✅ 3 modèles comparés
│   - RandomForest     │ ✅ Meilleur sélectionné
│   - GradientBoosting│ ✅ Métriques calculées
│   - LogisticReg     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   ÉTAPE 2: Files     │
│   Vérification       │ ✅ model.pkl
│                      │ ✅ production_metrics.json
│                      │ ✅ deployment_gcp/
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   ÉTAPE 3: Docker    │
│   Build & Test       │ ✅ Image construite
│                      │ ✅ Tests passés
│                      │ ✅ Prête à déployer
└──────────────────────┘
```

## 📦 Artifacts Générés

Chaque exécution génère des artifacts téléchargeables:

```
ml-pipeline-complete-outputs.zip
├── models/
│   ├── model.pkl              (Modèle entraîné)
│   └── production_metrics.json (Métriques)
└── deployment_gcp/
    ├── app.py                 (Application Flask)
    ├── Dockerfile             (Image GCP)
    ├── deploy.sh              (Script déploiement)
    └── README.md              (Documentation)
```

**Téléchargement:**
1. Aller sur GitHub → Actions
2. Cliquer sur une exécution réussie
3. Descendre à "Artifacts"
4. Télécharger `ml-pipeline-complete-outputs`

## 📊 Badges de Statut

Ajoutez ce badge dans votre README principal:

```markdown
![ML Pipeline](https://github.com/VOTRE-USERNAME/VOTRE-REPO/actions/workflows/docker-build.yml/badge.svg)
```

## 🚦 Indicateurs de Succès

### Dans les logs, vous verrez:

```
═══════════════════════════════════════════════════════════════
🤖 ÉTAPE 1: ENTRAÎNEMENT DES MODÈLES ML
═══════════════════════════════════════════════════════════════
✅ Données chargées: 9878 applications
📊 RandomForest: Accuracy 1.0000
📊 GradientBoosting: Accuracy 1.0000
📊 LogisticRegression: Accuracy 0.7890
🏆 MEILLEUR MODÈLE: RandomForest
✅ ÉTAPE 1 TERMINÉE

═══════════════════════════════════════════════════════════════
📂 ÉTAPE 2: VÉRIFICATION DES FICHIERS GÉNÉRÉS
═══════════════════════════════════════════════════════════════
✅ Modèle créé: models/model.pkl (137KB)
✅ Métriques créées
✅ Dossier GCP créé
✅ ÉTAPE 2 TERMINÉE

═══════════════════════════════════════════════════════════════
🐳 ÉTAPE 3: CONSTRUCTION DE L'IMAGE DOCKER
═══════════════════════════════════════════════════════════════
🏗️ Construction de l'image avec docker-compose...
✅ ÉTAPE 3 TERMINÉE

╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🎉 PIPELINE COMPLET RÉUSSI! 🎉                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## 🔍 Dépannage

### Le workflow Docker échoue:

```yaml
# Vérifier que Dockerfile.pipeline existe
ls -la Dockerfile.pipeline

# Tester localement
docker build -f Dockerfile.pipeline -t test-pipeline .
```

### Le workflow de test échoue:

```bash
# Vérifier les dépendances
pip install -r requirements.txt

# Tester localement
python src/train_pipeline_complete.py
```

### Cache Docker lent:

Les workflows utilisent GitHub Actions Cache (`gha`) pour accélérer les builds.
Le cache est automatique et se réinitialise après 7 jours d'inactivité.

## 📚 Ressources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Action](https://github.com/docker/build-push-action)
- [Python Setup Action](https://github.com/actions/setup-python)

## 🎯 Prochaines Étapes

Pour activer les workflows:

1. **Initialiser Git** (si pas déjà fait):
   ```bash
   git init
   git add .
   git commit -m "Initial commit with CI/CD"
   ```

2. **Créer un repo GitHub**:
   ```bash
   gh repo create mlops-jupyter --public --source=. --remote=origin --push
   ```

3. **Pousser le code**:
   ```bash
   git push -u origin main
   ```

4. **Vérifier les workflows**:
   - Aller sur https://github.com/votre-username/mlops-jupyter/actions
   - Les workflows devraient se lancer automatiquement!

## ✅ Avantages

- 🚀 **Build automatique** de l'image Docker
- 🧪 **Tests automatiques** du pipeline
- 📦 **Artifacts sauvegardés** (modèles, métriques)
- 🔄 **CI/CD complet** pour MLOps
- ⚡ **Cache intelligent** pour builds rapides
- 📊 **Rapports détaillés** des exécutions

---

**Note**: Ces workflows sont configurés pour fonctionner sans secrets. Pour Docker Hub push, ajoutez les secrets mentionnés ci-dessus.
