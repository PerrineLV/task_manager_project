import json
from typing import List, Optional
from .task import Task, Priority, Status

class TaskManager:
    """Gestionnaire principal des tâches"""
    def __init__(self, storage_file="tasks.json"):
        # Initialise la liste des tâches vide et définit le fichier de stockage par défaut
        self.tasks = []
        self.storage_file = storage_file

    def add_task(self, title, description="", priority=Priority.MEDIUM):
        # Crée une nouvelle tâche avec les paramètres fournis et l'ajoute à la liste
        # Retourne l'ID unique de la tâche créée
        task = Task(title, description, priority)
        self.tasks.append(task)
        return task.id

    def get_task(self, task_id) -> Optional[Task]:
        # Recherche et retourne une tâche par son ID unique
        # Retourne None si aucune tâche n'est trouvée
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_tasks_by_status(self, status: Status) -> List[Task]:
        # Filtre et retourne toutes les tâches ayant le statut spécifié
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        # Filtre et retourne toutes les tâches ayant la priorité spécifiée
        return [task for task in self.tasks if task.priority == priority]

    def delete_task(self, task_id) -> bool:
        # Supprime une tâche de la liste en utilisant son ID
        # Retourne True si la tâche a été trouvée et supprimée, False sinon
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True
        return False

    def save_to_file(self, filename=None):
        # Sauvegarde toutes les tâches au format JSON dans un fichier
        # Gère les erreurs d'écriture en levant une exception explicite
        filename = filename or self.storage_file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                tasks_data = [task.to_dict() for task in self.tasks]
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            raise Exception(f"Erreur lors de la sauvegarde: {e}")

    def load_from_file(self, filename=None):
        # Charge les tâches depuis un fichier JSON et les reconstitue en objets Task
        # Gère le cas où le fichier n'existe pas en initialisant une liste vide
        filename = filename or self.storage_file
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
        except FileNotFoundError:
            # Si le fichier n'existe pas, on commence avec une liste vide
            self.tasks = []
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise Exception(f"Erreur lors du chargement: {e}")

    def get_statistics(self):
        # Calcule et retourne les statistiques complètes des tâches :
        # - Nombre total de tâches
        # - Nombre de tâches terminées
        # - Répartition par priorité
        # - Répartition par statut
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task.status == Status.DONE])
        
        # Comptage par priorité
        tasks_by_priority = {}
        for priority in Priority:
            tasks_by_priority[priority.value] = len([task for task in self.tasks if task.priority == priority])
        
        # Comptage par statut
        tasks_by_status = {}
        for status in Status:
            tasks_by_status[status.value] = len([task for task in self.tasks if task.status == status])
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "tasks_by_priority": tasks_by_priority,
            "tasks_by_status": tasks_by_status
        }