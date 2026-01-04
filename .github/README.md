# 🚀 GitHub Actions - CI/CD Pipeline

Ce dossier contient les workflows GitHub Actions pour automatiser le build et les tests du pipeline ML.

## 📋 Workflows Disponibles

### 1. 🐳 Build ML Pipeline Docker Image (`docker-build.yml`)

**Déclenchement:**
- Push sur `main` ou `master`
- Modification des fichiers: `src/**`, `Dockerfile.pipeline`, `requirements.txt`
- Manuellement via l'interface GitHub

**Actions:**
- ✅ Construction de l'image Docker
- ✅ Tests de l'image
- ✅ Utilisation du cache pour builds rapides
- ✅ Affichage de la taille de l'image

**Utilisation manuelle:**
1. Aller sur GitHub → Actions
2. Sélectionner "Build ML Pipeline Docker Image"
3. Cliquer sur "Run workflow"

### 2. 🧪 Test ML Pipeline (`test-pipeline.yml`)

**Déclenchement:**
- Push sur `main` ou `master`
- Pull requests
- Manuellement

**Actions:**
- ✅ Installation des dépendances Python
- ✅ Exécution du pipeline ML
- ✅ Vérification des fichiers générés
- ✅ Upload des artifacts (modèles, métriques)
- ✅ Services PostgreSQL pour MLflow

**Artifacts générés:**
- `models/model.pkl` - Modèle entraîné
- `models/production_metrics.json` - Métriques du modèle
- `deployment_gcp/` - Fichiers de déploiement GCP

## 🔧 Configuration

### Secrets GitHub (Optionnels)

Pour pusher l'image sur Docker Hub, configurez ces secrets:

1. Aller sur GitHub → Settings → Secrets and variables → Actions
2. Ajouter:
   - `DOCKER_USERNAME`: Votre nom d'utilisateur Docker Hub
   - `DOCKER_PASSWORD`: Votre token Docker Hub

## 📊 Badges de Statut

Ajoutez ces badges dans votre README principal:

```markdown
![Build Docker](https://github.com/VOTRE-USERNAME/VOTRE-REPO/actions/workflows/docker-build.yml/badge.svg)
![Test Pipeline](https://github.com/VOTRE-USERNAME/VOTRE-REPO/actions/workflows/test-pipeline.yml/badge.svg)
```

## 🚦 Statut des Workflows

Les workflows s'affichent dans l'onglet **Actions** de votre repository GitHub.

### Indicateurs de succès:
- ✅ **Vert** - Build/Test réussi
- ❌ **Rouge** - Échec (voir les logs)
- 🟡 **Jaune** - En cours d'exécution

## 📈 Utilisation

### Vérifier le statut des builds:

```bash
# Cloner le repo
git clone https://github.com/votre-username/mlops-jupyter.git
cd mlops-jupyter

# Voir l'historique des commits
git log --oneline -n 5

# Pousser des changements (déclenche les workflows)
git add .
git commit -m "Update pipeline"
git push origin main
```

### Télécharger les artifacts:

1. Aller sur GitHub → Actions
2. Cliquer sur un workflow réussi
3. Descendre à "Artifacts"
4. Télécharger `pipeline-outputs`

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
