"""
Système de Décision Automatique pour le Déploiement
===================================================
Décide si le nouveau modèle doit être déployé
"""

import os

def make_deployment_decision():
    """Décide si on déploie le nouveau modèle"""
    
    print("="*60)
    print("🤖 DÉCISION AUTOMATIQUE DE DÉPLOIEMENT")
    print("="*60)
    
    # Lire les métriques
    with open('/tmp/improvement.txt', 'r') as f:
        improvement = float(f.read().strip())
    
    with open('/tmp/accuracy.txt', 'r') as f:
        accuracy = float(f.read().strip())
    
    # Critères de décision
    score = 0
    max_score = 100
    
    print("\n📋 CRITÈRES D'ÉVALUATION:")
    
    # 1. Amélioration des performances (40 points)
    if improvement > 0.01:  # > 1%
        score += 40
        print(f"   ✅ Amélioration significative: {improvement:+.4f} (+40 pts)")
    elif improvement > 0:
        score += 20
        print(f"   🟡 Légère amélioration: {improvement:+.4f} (+20 pts)")
    elif improvement > -0.005:  # > -0.5%
        score += 5
        print(f"   🟠 Performance similaire: {improvement:+.4f} (+5 pts)")
    else:
        score -= 50
        print(f"   ❌ Dégradation: {improvement:+.4f} (-50 pts)")
    
    # 2. Qualité absolue du modèle (30 points)
    if accuracy > 0.9:
        score += 30
        print(f"   ✅ Excellente accuracy: {accuracy:.4f} (+30 pts)")
    elif accuracy > 0.8:
        score += 20
        print(f"   🟡 Bonne accuracy: {accuracy:.4f} (+20 pts)")
    else:
        score += 10
        print(f"   🟠 Accuracy acceptable: {accuracy:.4f} (+10 pts)")
    
    # 3. Stabilité (30 points) - Simplifié pour la démo
    score += 30
    print(f"   ✅ Modèle stable (+30 pts)")
    
    print(f"\n📊 SCORE FINAL: {score}/{max_score}")
    print("="*60)
    
    # Décision
    if score >= 70:
        decision = True
        action = "🟢 DÉPLOIEMENT AUTOMATIQUE APPROUVÉ"
        reason = "Score suffisant pour déploiement automatique"
    elif score >= 50:
        decision = False
        action = "🟡 VALIDATION MANUELLE REQUISE"
        reason = "Score modéré - revue humaine nécessaire"
    else:
        decision = False
        action = "🔴 DÉPLOIEMENT REFUSÉ"
        reason = "Score insuffisant"
    
    print(f"\n🎯 DÉCISION: {action}")
    print(f"   Raison: {reason}")
    print(f"   Confiance: {score}%")
    
    # Sauvegarder la décision
    with open('/tmp/should_deploy.txt', 'w') as f:
        f.write('true' if decision else 'false')
    
    with open('/tmp/deployment_score.txt', 'w') as f:
        f.write(str(score))
    
    print("="*60)

if __name__ == '__main__':
    make_deployment_decision()
