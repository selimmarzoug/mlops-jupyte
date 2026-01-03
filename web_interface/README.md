# 🌐 Interface Web - Ajout de Données

Interface web simple pour ajouter des applications au pipeline MLOps sans modifier manuellement le CSV.

## 🚀 Démarrage Rapide

```bash
# 1. Installer les dépendances
cd web_interface
pip install -r requirements.txt

# 2. Lancer l'interface
python app.py
```

**Interface accessible à**: http://localhost:5001

## ✨ Fonctionnalités

### 1. Ajout Manuel
- Formulaire convivial pour ajouter une app
- Validation des champs obligatoires
- Détection des doublons
- Mise à jour automatique du CSV

### 2. Upload CSV en Masse
- Upload d'un fichier CSV avec plusieurs apps
- Fusion automatique avec les données existantes
- Suppression des doublons

### 3. Statistiques en Temps Réel
- Nombre total d'applications
- Nombre de catégories
- État du pipeline

## 📋 Format des Données

Les champs du formulaire:
- **Nom de l'App*** (obligatoire)
- **Catégorie*** (obligatoire)
- Note (0-5)
- Nombre d'avis
- Taille (ex: 25M)
- Installations (ex: 10,000+)
- Type (Gratuit/Payant)
- Prix
- Classification (Everyone, Teen, etc.)
- Genre
- Version actuelle
- Version Android requise

## 🔄 Intégration avec le Pipeline

Chaque ajout:
1. ✅ Ajoute les données dans `data/googleplaystore_clean.csv`
2. ✅ Log l'opération dans `logs/data_additions.log`
3. ✅ Si ≥100 nouvelles apps → Déclenche le pipeline automatiquement (via Git push)

## 🎯 Workflow Utilisateur

### Ajout Manuel
```
1. Ouvrir http://localhost:5001
2. Remplir le formulaire
3. Cliquer "Ajouter l'Application"
4. ✅ App ajoutée au CSV!
```

### Upload en Masse
```
1. Préparer un CSV avec les nouvelles apps
2. Aller sur l'onglet "Upload CSV"
3. Sélectionner le fichier
4. Cliquer "Upload et Ajouter"
5. ✅ Toutes les apps ajoutées!
```

### Déclencher le Pipeline
```bash
# Une fois que vous avez ajouté ≥100 apps:
git add data/googleplaystore_clean.csv
git commit -m "feat: ajout de nouvelles applications via interface web"
git push origin main

# → GitHub Actions démarre automatiquement!
```

## 📊 API Endpoints

```bash
# Page d'accueil
GET http://localhost:5001/

# Ajouter une app
POST http://localhost:5001/add_app
Content-Type: application/x-www-form-urlencoded

# Upload CSV
POST http://localhost:5001/bulk_upload
Content-Type: multipart/form-data

# Statistiques JSON
GET http://localhost:5001/stats

# Applications récentes
GET http://localhost:5001/recent_additions
```

## 🛠️ Exemple avec cURL

```bash
# Ajouter une app via API
curl -X POST http://localhost:5001/add_app \
  -d "app_name=MyApp" \
  -d "category=PRODUCTIVITY" \
  -d "rating=4.5" \
  -d "reviews=1000"

# Voir les stats
curl http://localhost:5001/stats

# Voir les récentes
curl http://localhost:5001/recent_additions
```

## 🔧 Configuration

Modifier dans `app.py`:
```python
# Port du serveur
app.run(host='0.0.0.0', port=5001, debug=True)

# Chemin du fichier CSV
DATA_FILE = '../data/googleplaystore_clean.csv'

# Fichier de logs
LOG_FILE = '../logs/data_additions.log'
```

## 🐳 Docker (Optionnel)

```dockerfile
# Ajouter dans docker-compose.yml
web-interface:
  build:
    context: ./web_interface
  ports:
    - "5001:5001"
  volumes:
    - ./data:/app/data
    - ./logs:/app/logs
```

## 🎨 Personnalisation

L'interface utilise des couleurs personnalisables dans `templates/index.html`:
```css
/* Gradient principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Couleurs */
--primary: #667eea;
--secondary: #764ba2;
```

## 📝 Logs

Les logs sont sauvegardés dans `logs/data_additions.log`:
```
2026-01-03 14:30:00 - INFO - Nouvelle app ajoutée: WhatsApp - Catégorie: COMMUNICATION
2026-01-03 14:35:00 - INFO - Upload en masse: 50 nouvelles apps ajoutées
```

## 🔒 Sécurité (Production)

Pour un environnement de production, ajoutez:
```python
# Authentification
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# HTTPS
app.run(ssl_context='adhoc')

# Rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])
```

## 🎉 Résumé

- ✅ Interface conviviale
- ✅ Ajout manuel ou en masse
- ✅ Validation et détection doublons
- ✅ Intégration automatique avec le pipeline
- ✅ Stats en temps réel
- ✅ API REST disponible

**Plus besoin de modifier le CSV à la main!** 🚀
