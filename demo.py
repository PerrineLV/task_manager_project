#!/usr/bin/env python3
"""
Démonstration du module TaskManager
"""
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status
from src.task_manager.services import EmailService

def main():
    print("=== Démonstration TaskManager ===\n")
    
    # 1. Création d'un gestionnaire de tâches
    print("1. Création du gestionnaire de tâches")
    manager = TaskManager("demo_tasks.json")
    print("✓ Gestionnaire créé\n")
    
    # 2. Ajout de plusieurs tâches avec différentes priorités
    print("2. Ajout de tâches avec différentes priorités")
    
    # Tâches avec différentes priorités
    task1_id = manager.add_task(
        "Préparer la présentation",
        "Créer les slides pour la réunion client",
        Priority.HIGH
    )
    print(f"✓ Tâche HIGH ajoutée (ID: {task1_id})")
    
    task2_id = manager.add_task(
        "Répondre aux emails",
        "Traiter la boîte de réception",
        Priority.MEDIUM
    )
    print(f"✓ Tâche MEDIUM ajoutée (ID: {task2_id})")
    
    task3_id = manager.add_task(
        "Corriger le bug critique",
        "Résoudre le problème de sécurité",
        Priority.URGENT
    )
    print(f"✓ Tâche URGENT ajoutée (ID: {task3_id})")
    
    task4_id = manager.add_task(
        "Organiser le bureau",
        "Ranger les documents",
        Priority.LOW
    )
    print(f"✓ Tâche LOW ajoutée (ID: {task4_id})")
    
    task5_id = manager.add_task(
        "Planifier les vacances",
        "Réserver l'hôtel et les vols",
        Priority.MEDIUM
    )
    print(f"✓ Tâche MEDIUM ajoutée (ID: {task5_id})\n")
    
    # 3. Marquer certaines tâches comme terminées
    print("3. Marquage de certaines tâches comme terminées")
    
    # Marquer la tâche email comme terminée
    task2 = manager.get_task(task2_id)
    if task2:
        task2.mark_completed()
        print(f"✓ Tâche '{task2.title}' marquée comme terminée")
    
    # Marquer la tâche bureau comme terminée
    task4 = manager.get_task(task4_id)
    if task4:
        task4.mark_completed()
        print(f"✓ Tâche '{task4.title}' marquée comme terminée\n")
    
    # 4. Affichage des statistiques
    print("4. Affichage des statistiques")
    stats = manager.get_statistics()
    
    print(f"📊 Statistiques des tâches :")
    print(f"   - Total des tâches : {stats['total_tasks']}")
    print(f"   - Tâches terminées : {stats['completed_tasks']}")
    print(f"   - Taux de completion : {stats['completed_tasks']/stats['total_tasks']*100:.1f}%")
    
    print(f"\n📈 Répartition par priorité :")
    for priority, count in stats['tasks_by_priority'].items():
        print(f"   - {priority.upper()} : {count} tâche(s)")
    
    print(f"\n📋 Répartition par statut :")
    for status, count in stats['tasks_by_status'].items():
        print(f"   - {status.upper()} : {count} tâche(s)")
    
    # Afficher le détail des tâches
    print(f"\n📝 Détail des tâches :")
    for task in manager.tasks:
        status_emoji = "✅" if task.status == Status.DONE else "⏳"
        priority_emoji = {
            Priority.LOW: "🟢",
            Priority.MEDIUM: "🟡", 
            Priority.HIGH: "🟠",
            Priority.URGENT: "🔴"
        }[task.priority]
        print(f"   {status_emoji} {priority_emoji} {task.title}")
        print(f"      Description: {task.description}")
        print(f"      Créée le: {task.created_at.strftime('%d/%m/%Y à %H:%M')}")
        if task.completed_at:
            print(f"      Terminée le: {task.completed_at.strftime('%d/%m/%Y à %H:%M')}")
        print()
    
    # 5. Sauvegarde dans un fichier
    print("5. Sauvegarde des tâches dans un fichier")
    try:
        manager.save_to_file()
        print("✓ Sauvegarde réussie dans 'demo_tasks.json'\n")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}\n")
    
    # 6. Rechargement et vérification
    print("6. Rechargement et vérification")
    
    # Créer un nouveau gestionnaire pour tester le chargement
    new_manager = TaskManager("demo_tasks.json")
    print("✓ Nouveau gestionnaire créé")
    
    try:
        new_manager.load_from_file()
        print("✓ Tâches rechargées depuis le fichier")
        
        # Vérifier que les données sont identiques
        if len(new_manager.tasks) == len(manager.tasks):
            print(f"✓ Nombre de tâches correct: {len(new_manager.tasks)}")
            
            # Vérifier quelques propriétés
            reloaded_stats = new_manager.get_statistics()
            if reloaded_stats['total_tasks'] == stats['total_tasks']:
                print("✓ Statistiques cohérentes après rechargement")
            else:
                print("❌ Incohérence dans les statistiques")
                
            # Vérifier les tâches terminées
            completed_tasks = [t for t in new_manager.tasks if t.status == Status.DONE]
            print(f"✓ {len(completed_tasks)} tâche(s) terminée(s) après rechargement")
            
        else:
            print("❌ Problème lors du rechargement: nombre de tâches différent")
            
    except Exception as e:
        print(f"❌ Erreur lors du rechargement: {e}")
    
    # Démonstration du service email (configuration uniquement)
    print("\n7. Configuration du service email")
    email_service = EmailService()
    email_service.configure_credentials("demo@example.com", "password123")
    print("✓ Service email configuré (pour démonstration)\n")
    
    print("🎉 Démonstration terminée avec succès !")
    print("   - Gestionnaire de tâches opérationnel")
    print("   - Tâches créées, modifiées et sauvegardées")
    print("   - Statistiques générées")
    print("   - Persistance des données vérifiée")


if __name__ == "__main__":
    main()