# Dockerfile pour déployer l'interface de prédiction sur Google Cloud Run
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .
COPY templates/ templates/

# Créer le répertoire models
RUN mkdir -p models

# Copier le modèle (si disponible)
COPY model.pkl models/model.pkl

# Variables d'environnement
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Exposer le port
EXPOSE 8080

# Commande de démarrage
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
