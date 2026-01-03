"""
Génération de rapport de performance
====================================
"""

import os
import json
from datetime import datetime

def generate_report():
    """Génère un rapport de performance"""
    
    print("📝 Génération du rapport...")
    
    # Lire les métriques
    try:
        with open('/tmp/accuracy.txt', 'r') as f:
            accuracy = f.read().strip()
        with open('/tmp/improvement.txt', 'r') as f:
            improvement = f.read().strip()
        with open('/tmp/model_version.txt', 'r') as f:
            version = f.read().strip()
    except:
        print("⚠️  Fichiers de métriques non trouvés")
        return
    
    # Créer le rapport
    report = {
        'timestamp': datetime.now().isoformat(),
        'version': version,
        'metrics': {
            'accuracy': accuracy,
            'improvement': improvement
        }
    }
    
    # Sauvegarder
    os.makedirs('reports', exist_ok=True)
    report_path = f'reports/report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Rapport généré: {report_path}")

if __name__ == '__main__':
    generate_report()
