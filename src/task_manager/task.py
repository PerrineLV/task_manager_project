import time
from datetime import datetime
from enum import Enum


class Priority(Enum):
    # Définition des priorités (LOW, MEDIUM, HIGH, URGENT)
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Status(Enum):
    # Définition des statuts (TODO, IN_PROGRESS, DONE, CANCELLED)
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class Task:
    """Une tâche avec toutes ses propriétés"""

    def __init__(self, title, description="", priority=Priority.MEDIUM):
        # Validation des paramètres
        if not title or not title.strip():
            raise ValueError("Le titre ne peut pas être vide")

        if not isinstance(priority, Priority):
            raise ValueError("La priorité doit être une instance de Priority")

        # Initialisation des attributs
        self.id = time.time()
        self.title = title.strip()
        self.description = description
        self.priority = priority
        self.status = Status.TODO
        self.created_at = datetime.now()
        self.completed_at = None
        self.project_id = None

    def mark_completed(self):
        # Changement du statut à DONE
        self.status = Status.DONE
        # Ajout de completed_at avec datetime.now()
        self.completed_at = datetime.now()

    def update_priority(self, new_priority):
        # Validation et mise à jour de la priorité
        if not isinstance(new_priority, Priority):
            raise ValueError("La nouvelle priorité doit être une instance de Priority")
        self.priority = new_priority

    def assign_to_project(self, project_id):
        # Assignation de la tâche à un projet
        self.project_id = project_id

    def to_dict(self):
        # Retour d'un dictionnaire pour la sérialisation JSON
        # Gestion de la conversion des Enum et datetime
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "project_id": self.project_id,
        }

    @classmethod
    def from_dict(cls, data):
        # Création d'une Task depuis un dictionnaire
        # Gestion de la conversion des string vers Enum et datetime
        task = cls(
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority[data["priority"].upper()],
        )

        # Restauration des autres attributs
        task.id = data["id"]
        task.status = Status[data["status"].upper()]
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.completed_at = (
            datetime.fromisoformat(data["completed_at"])
            if data.get("completed_at")
            else None
        )
        task.project_id = data.get("project_id")

        return task
