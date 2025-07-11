import pytest
from datetime import datetime
from src.task_manager.task import Task, Priority, Status

class TestTaskCreation:
    """Tests de création de tâches"""
    def test_create_task_minimal(self):
        """Test création tâche avec paramètres minimaux"""
        task = Task("Test Task")
        
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == Priority.MEDIUM
        assert task.status == Status.TODO
        assert task.completed_at is None
        assert task.project_id is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.id, float)

    def test_create_task_complete(self):
        """Test création tâche avec tous les paramètres"""
        task = Task("Complete Task", "Description test", Priority.HIGH)
        
        assert task.title == "Complete Task"
        assert task.description == "Description test"
        assert task.priority == Priority.HIGH
        assert task.status == Status.TODO
        assert task.completed_at is None
        assert task.project_id is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.id, float)

    def test_create_task_empty_title_raises_error(self):
        """Test titre vide lève une erreur"""
        with pytest.raises(ValueError, match="Le titre ne peut pas être vide"):
            Task("")

    def test_create_task_whitespace_title_raises_error(self):
        """Test titre avec espaces seulement lève une erreur"""
        with pytest.raises(ValueError, match="Le titre ne peut pas être vide"):
            Task("   ")

    def test_create_task_invalid_priority_raises_error(self):
        """Test priorité invalide lève une erreur"""
        with pytest.raises(ValueError, match="La priorité doit être une instance de Priority"):
            Task("Test Task", priority="high")

class TestTaskOperations:
    """Tests des opérations sur les tâches"""
    def setup_method(self):
        """Fixture : tâche de test"""
        self.task = Task("Test Task", "Description test", Priority.MEDIUM)

    def test_mark_completed_changes_status(self):
        """Test marquage comme terminée change le statut"""
        self.task.mark_completed()
        
        assert self.task.status == Status.DONE

    def test_mark_completed_sets_completed_at(self):
        """Test marquage comme terminée définit completed_at"""
        self.task.mark_completed()
        
        assert self.task.completed_at is not None
        assert isinstance(self.task.completed_at, datetime)

    def test_update_priority_valid(self):
        """Test mise à jour priorité valide"""
        self.task.update_priority(Priority.HIGH)
        
        assert self.task.priority == Priority.HIGH

    def test_update_priority_invalid_raises_error(self):
        """Test mise à jour priorité invalide lève une erreur"""
        with pytest.raises(ValueError, match="La nouvelle priorité doit être une instance de Priority"):
            self.task.update_priority("high")

    def test_assign_to_project(self):
        """Test assignation à un projet"""
        self.task.assign_to_project("project-123")
        
        assert self.task.project_id == "project-123"

class TestTaskSerialization:
    """Tests de sérialisation JSON"""
    def setup_method(self):
        """Fixture : tâche complexe avec tous les attributs"""
        self.task = Task("Complex Task", "Description complète", Priority.HIGH)
        self.task.assign_to_project("project-456")
        self.task.mark_completed()

    def test_to_dict_contains_all_fields(self):
        """Test conversion en dictionnaire contient tous les champs"""
        task_dict = self.task.to_dict()
        
        expected_keys = {"id", "title", "description", "priority", "status", 
                        "created_at", "completed_at", "project_id"}
        assert set(task_dict.keys()) == expected_keys

    def test_to_dict_enum_values_are_strings(self):
        """Test conversion en dictionnaire a des valeurs Enum en string"""
        task_dict = self.task.to_dict()
        
        assert isinstance(task_dict["priority"], str)
        assert isinstance(task_dict["status"], str)

    def test_to_dict_datetime_values_are_strings(self):
        """Test conversion en dictionnaire a des valeurs datetime en string"""
        task_dict = self.task.to_dict()
        
        assert isinstance(task_dict["created_at"], str)
        assert isinstance(task_dict["completed_at"], str)

    def test_from_dict_recreates_task_correctly(self):
        """Test recréation depuis dictionnaire reproduit la tâche"""
        task_dict = self.task.to_dict()
        recreated_task = Task.from_dict(task_dict)
        
        assert recreated_task.id == self.task.id
        assert recreated_task.title == self.task.title
        assert recreated_task.description == self.task.description
        assert recreated_task.priority == self.task.priority
        assert recreated_task.status == self.task.status
        assert recreated_task.created_at == self.task.created_at
        assert recreated_task.completed_at == self.task.completed_at
        assert recreated_task.project_id == self.task.project_id