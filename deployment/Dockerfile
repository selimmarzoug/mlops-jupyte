# Dockerfile pour Google Cloud Run
FROM python:3.8-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=True
ENV PORT=8080
ENV MODEL_URI=models:/google-playstore-success-predictor/Production
ENV MLFLOW_TRACKING_URI=http://host.docker.internal:5000

# Répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
COPY app.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port
EXPOSE 8080

# Santé check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Démarrer avec gunicorn (production-ready)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
