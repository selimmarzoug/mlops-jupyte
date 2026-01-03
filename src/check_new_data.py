"""
Script pour détecter les nouvelles données
==========================================
Vérifie si de nouvelles applications ont été ajoutées
"""

import os
import pandas as pd
from datetime import datetime, timedelta

def check_new_data():
    """Vérifie si de nouvelles données sont disponibles"""
    
    # Chemins des fichiers
    data_path = 'data/googleplaystore_clean.csv'
    last_train_file = 'models/last_training_date.txt'
    
    # Charger les données
    try:
        df = pd.read_csv(data_path)
        current_data_count = len(df)
        print(f"📊 Données actuelles: {current_data_count} applications")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des données: {e}")
        with open('/tmp/has_new_data.txt', 'w') as f:
            f.write('false')
        with open('/tmp/new_data_count.txt', 'w') as f:
            f.write('0')
        return
    
    # Vérifier la dernière date d'entraînement
    if os.path.exists(last_train_file):
        with open(last_train_file, 'r') as f:
            last_count = int(f.read().strip())
        
        new_data_count = current_data_count - last_count
        print(f"➕ Nouvelles applications: {new_data_count}")
        
        # Seuil: au moins 100 nouvelles applications
        threshold = 100
        has_new_data = new_data_count >= threshold
        
        if has_new_data:
            print(f"✅ Seuil atteint ({new_data_count} >= {threshold})")
        else:
            print(f"⏳ Seuil non atteint ({new_data_count} < {threshold})")
    else:
        # Première fois - toujours réentraîner
        print("🆕 Première exécution - réentraînement nécessaire")
        new_data_count = current_data_count
        has_new_data = True
    
    # Écrire les résultats
    with open('/tmp/has_new_data.txt', 'w') as f:
        f.write('true' if has_new_data else 'false')
    
    with open('/tmp/new_data_count.txt', 'w') as f:
        f.write(str(new_data_count))
    
    print(f"\n{'='*60}")
    print(f"Résultat: {'✅ Réentraînement nécessaire' if has_new_data else '⏳ Attendre plus de données'}")
    print(f"{'='*60}")

if __name__ == '__main__':
    check_new_data()
