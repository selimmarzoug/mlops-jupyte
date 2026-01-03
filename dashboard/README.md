# 📊 Dashboard Automatique - Résultats MLOps

## 🎯 Vue d'Ensemble

Dashboard automatique qui affiche les résultats du **meilleur modèle déployé** après chaque exécution du pipeline MLOps.

---

## 🚀 Démarrage Automatique

### Option 1: Script Automatique (Recommandé)
```bash
./start_dashboard.sh
```

Le dashboard démarre automatiquement en arrière-plan!

### Option 2: Manuel
```bash
cd dashboard
python3 app.py
```

---

## 🌐 Accès au Dashboard

**URL principale**: http://localhost:5002

### Endpoints Disponibles

| Endpoint | Description |
|----------|-------------|
| `/` | Dashboard visuel complet |
| `/api/model` | Infos du modèle (JSON) |
| `/api/stats` | Statistiques des données (JSON) |
| `/api/comparison` | Comparaison production vs candidat (JSON) |
| `/health` | Health check |

---

## 📊 Fonctionnalités

### 1. Informations du Modèle en Production
- **Type** de modèle (RandomForest, LogisticRegression, etc.)
- **Taille** du fichier
- **Date** de déploiement
- **Paramètres** (n_estimators, max_depth, etc.)

### 2. Métriques de Performance
- ✅ **Accuracy** (avec barre de progression)
- 📊 **Precision**
- 📈 **Recall**
- 🎯 **F1-Score**

Chaque métrique est colorée:
- 🟢 Vert: Excellente (≥85%)
- 🟡 Jaune: Bonne (75-85%)
- 🔴 Rouge: À améliorer (<75%)

### 3. Statistiques des Données
- Nombre total d'applications
- Nombre de catégories
- Dernière mise à jour
- Seuil de réentraînement

### 4. Comparaison des Modèles
- **Production** vs **Candidat**
- Tableau comparatif automatique
- Indication du gagnant pour chaque métrique

---

## 🔄 Workflow Automatique

### Après Chaque Pipeline GitHub Actions:

1. **Pipeline termine** ✅
2. **Modèle déployé** (si score ≥ 70/100)
3. **Dashboard se met à jour** automatiquement
4. **Rapport HTML généré** dans `reports/`

### Accès aux Résultats:

**Immédiat** (après déploiement):
```bash
# Lancer le dashboard
./start_dashboard.sh

# Ouvrir: http://localhost:5002
```

**Via GitHub Actions**:
- Télécharger l'artifact "dashboard-report"
- Ouvrir le fichier HTML dans un navigateur

---

## 📁 Structure des Fichiers

```
dashboard/
├── app.py                      # Application Flask
├── templates/
│   └── dashboard.html         # Interface web
└── requirements.txt           # Dépendances

reports/
├── dashboard_report.html      # Dernier rapport
└── dashboard_report_*.html    # Rapports historiques

models/
├── production_model.pkl       # Modèle en production
├── production_metrics.json    # Métriques production
├── candidate_model.pkl        # Modèle candidat
└── candidate_metrics.json     # Métriques candidat
```

---

## 🔧 Configuration

### Changer le Port
Dans `dashboard/app.py`:
```python
app.run(host='0.0.0.0', port=5002, debug=True)
#                            ^^^^ changer ici
```

### Auto-Refresh
Le dashboard se rafraîchit:
- **Manuel**: Cliquez sur "🔄 Rafraîchir"
- **Auto**: Toutes les 30 secondes (timestamp)

---

## 🎨 Aperçu du Dashboard

```
┌─────────────────────────────────────────────────────────┐
│           🎯 MLOps Dashboard                            │
│     Résultats du Meilleur Modèle Déployé               │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │
│  │  Modèle en  │ │  Métriques  │ │   Données   │     │
│  │ Production  │ │     de      │ │ Entraînement│     │
│  │             │ │ Performance │ │             │     │
│  │ ✅ Déployé  │ │ Accuracy:   │ │ 9,309 apps  │     │
│  │             │ │   87.5%     │ │             │     │
│  │ RandomForest│ │ ████████░   │ │ 33 catég.   │     │
│  └─────────────┘ └─────────────┘ └─────────────┘     │
│                                                         │
│  ⚖️ Comparaison des Modèles                            │
│  ┌────────────────────────────────────────────────┐   │
│  │ Métrique │ Production │ Candidat │ Gagnant    │   │
│  ├──────────┼────────────┼──────────┼────────────┤   │
│  │ Accuracy │   87.5%    │  89.2%   │ 🏆 Candidat│   │
│  └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📡 API Usage

### Récupérer les Infos du Modèle
```bash
curl http://localhost:5002/api/model
```

**Réponse**:
```json
{
  "deployed": true,
  "model_type": "RandomForestClassifier",
  "size": "49.6 KB",
  "deployed_at": "2026-01-03 14:30:00",
  "n_estimators": 100,
  "max_depth": 10,
  "metrics": {
    "accuracy": 0.875,
    "precision": 0.882,
    "recall": 0.868,
    "f1_score": 0.875
  }
}
```

### Comparer les Modèles
```bash
curl http://localhost:5002/api/comparison
```

---

## 🐳 Docker (Optionnel)

Ajouter dans `docker-compose.yml`:
```yaml
dashboard:
  build: ./dashboard
  ports:
    - "5002:5002"
  volumes:
    - ./models:/app/models
    - ./data:/app/data
    - ./logs:/app/logs
    - ./reports:/app/reports
  depends_on:
    - mlflow
```

---

## 📝 Logs

Les logs du dashboard sont dans:
```bash
cat logs/dashboard.log
```

---

## 🛑 Arrêter le Dashboard

```bash
# Trouver le processus
lsof -i:5002

# Arrêter
kill -9 $(lsof -t -i:5002)
```

---

## 🎯 Intégration Complète

### Workflow Utilisateur:

1. **Ajouter des données** (via interface web: http://localhost:5001)
2. **Git push** → Déclenche le pipeline
3. **GitHub Actions** exécute le pipeline (3-5 min)
4. **Modèle déployé** automatiquement si performant
5. **Dashboard se met à jour** → Voir les résultats immédiatement!

```bash
# Tout en un: ajouter données → voir résultats
curl -X POST http://localhost:5001/add_app -d "app_name=MyApp&category=PRODUCTIVITY"
# ... ajouter 100+ apps

git add data/
git commit -m "feat: nouvelles apps"
git push

# Attendre 3-5 minutes

./start_dashboard.sh
# Ouvrir: http://localhost:5002
```

---

## ✨ Fonctionnalités Avancées

### Auto-Notifications (À venir)
- Slack: Notification après déploiement
- Email: Rapport HTML par email
- Discord/Teams: Intégrations disponibles

### Monitoring (À venir)
- Drift detection
- Performance degradation alerts
- A/B testing results

---

## 🎉 Résumé

**Dashboard 100% Automatique!**

✅ Se lance en une commande  
✅ Se met à jour automatiquement  
✅ Affiche les métriques en temps réel  
✅ Compare production vs candidat  
✅ API REST disponible  
✅ Interface moderne et responsive  

**Plus besoin de chercher les résultats dans les logs!** 🚀

---

## 🆘 Support

Des problèmes?

1. Vérifier que le port 5002 est libre: `lsof -i:5002`
2. Vérifier les logs: `cat logs/dashboard.log`
3. Relancer: `./start_dashboard.sh`

Pour les erreurs de dépendances:
```bash
pip install -r dashboard/requirements.txt --user
```
