"""
Script de Déploiement
=====================
Gère le déploiement du modèle en staging/production
"""

import os
import shutil
import argparse
from datetime import datetime

def deploy(environment='production', canary=1.0):
    """Déploie le modèle dans l'environnement spécifié"""
    
    print("="*60)
    print(f"🚀 DÉPLOIEMENT EN {environment.upper()}")
    print("="*60)
    
    candidate_model = 'models/candidate_model.pkl'
    
    if environment == 'staging':
        target_path = 'models/staging_model.pkl'
        print(f"\n📦 Copie du modèle vers staging...")
        shutil.copy(candidate_model, target_path)
        print(f"✅ Modèle déployé en staging: {target_path}")
    
    elif environment == 'production':
        if canary < 1.0:
            print(f"\n🐤 Déploiement CANARY: {canary*100:.0f}% du trafic")
            target_path = f'models/canary_model_{canary}.pkl'
        else:
            print(f"\n✅ Déploiement PRODUCTION COMPLET")
            # Backup de l'ancien modèle
            if os.path.exists('models/production_model.pkl'):
                backup_path = f"models/production_model_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
                shutil.copy('models/production_model.pkl', backup_path)
                print(f"💾 Backup créé: {backup_path}")
            
            target_path = 'models/production_model.pkl'
            
            # Copier les métriques
            if os.path.exists('/tmp/accuracy.txt'):
                with open('/tmp/accuracy.txt', 'r') as f:
                    accuracy = f.read().strip()
                with open('models/production_metrics.txt', 'w') as f:
                    f.write(accuracy)
        
        shutil.copy(candidate_model, target_path)
        print(f"✅ Modèle déployé: {target_path}")
    
    # Log du déploiement
    log_entry = f"{datetime.now().isoformat()} | {environment} | canary={canary}\n"
    os.makedirs('logs', exist_ok=True)
    with open('logs/deployment.log', 'a') as f:
        f.write(log_entry)
    
    print("\n" + "="*60)

def rollback():
    """Rollback vers la version précédente"""
    
    print("="*60)
    print("⚠️  ROLLBACK AUTOMATIQUE")
    print("="*60)
    
    # Chercher le dernier backup
    backups = [f for f in os.listdir('models') if f.startswith('production_model_backup_')]
    if backups:
        latest_backup = sorted(backups)[-1]
        backup_path = os.path.join('models', latest_backup)
        
        print(f"\n🔄 Restauration du backup: {latest_backup}")
        shutil.copy(backup_path, 'models/production_model.pkl')
        print("✅ Rollback effectué avec succès")
    else:
        print("❌ Aucun backup disponible")
    
    print("="*60)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Déploiement du modèle ML')
    parser.add_argument('--environment', choices=['staging', 'production'], default='production')
    parser.add_argument('--canary', type=float, default=1.0, help='Ratio du trafic (0.0 à 1.0)')
    parser.add_argument('--rollback', action='store_true', help='Effectuer un rollback')
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback()
    else:
        deploy(args.environment, args.canary)
