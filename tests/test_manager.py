import pytest
from unittest.mock import patch, mock_open
import json
from src.task_manager.manager import TaskManager
from src.task_manager.task import Task, Priority, Status

class TestTaskManagerBasics:
    """Tests basiques du gestionnaire"""
    def setup_method(self):
        """Fixture : gestionnaire de test"""
        # Création d'un gestionnaire de tâches avec un fichier de test
        self.manager = TaskManager("test_tasks.json")

    def test_add_task_returns_id(self):
        """Test ajout tâche retourne un ID"""
        # Ajout d'une nouvelle tâche avec titre, description et priorité
        task_id = self.manager.add_task("Test Task", "Test Description", Priority.HIGH)
        
        # Vérification que l'ID est retourné et est valide
        assert task_id is not None
        assert isinstance(task_id, (int, float))
        
        # Vérification que la tâche a été ajoutée à la liste avec les bonnes propriétés
        assert len(self.manager.tasks) == 1
        assert self.manager.tasks[0].id == task_id
        assert self.manager.tasks[0].title == "Test Task"
        assert self.manager.tasks[0].description == "Test Description"
        assert self.manager.tasks[0].priority == Priority.HIGH

    def test_get_task_existing(self):
        """Test récupération tâche existante"""
        # Création d'une tâche pour les tests
        task_id = self.manager.add_task("Test Task", "Test Description", Priority.MEDIUM)
        
        # Récupération de la tâche par son ID
        retrieved_task = self.manager.get_task(task_id)
        
        # Vérification que la tâche récupérée a les bonnes propriétés
        assert retrieved_task is not None
        assert retrieved_task.id == task_id
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.description == "Test Description"
        assert retrieved_task.priority == Priority.MEDIUM
        assert retrieved_task.status == Status.TODO

    def test_get_task_nonexistent_returns_none(self):
        """Test récupération tâche inexistante"""
        # Tentative de récupération d'une tâche avec un ID qui n'existe pas
        non_existent_task = self.manager.get_task(999999)
        
        # Vérification que None est retourné pour une tâche inexistante
        assert non_existent_task is None

class TestTaskManagerFiltering:
    """Tests de filtrage des tâches"""
    def setup_method(self):
        """Fixture : gestionnaire avec plusieurs tâches"""
        self.manager = TaskManager("test_tasks.json")
        # Création de plusieurs tâches avec différents statuts et priorités pour les tests
        self.task1_id = self.manager.add_task("Task 1", "Description 1", Priority.HIGH)
        self.task2_id = self.manager.add_task("Task 2", "Description 2", Priority.LOW)
        self.task3_id = self.manager.add_task("Task 3", "Description 3", Priority.MEDIUM)
        self.task4_id = self.manager.add_task("Task 4", "Description 4", Priority.HIGH)
        
        # Modification des statuts pour créer une variété de cas de test
        task1 = self.manager.get_task(self.task1_id)
        task1.status = Status.IN_PROGRESS
        
        task2 = self.manager.get_task(self.task2_id)
        task2.mark_completed()
        
        task3 = self.manager.get_task(self.task3_id)
        task3.status = Status.CANCELLED

    def test_get_tasks_by_status(self):
        """Test filtrage par statut"""
        # Filtrage des tâches par statut TODO et vérification du résultat
        todo_tasks = self.manager.get_tasks_by_status(Status.TODO)
        
        # Vérification qu'une seule tâche a le statut TODO (task4)
        assert len(todo_tasks) == 1
        assert todo_tasks[0].id == self.task4_id
        assert todo_tasks[0].status == Status.TODO
        
        # Test de filtrage avec le statut DONE
        done_tasks = self.manager.get_tasks_by_status(Status.DONE)
        assert len(done_tasks) == 1
        assert done_tasks[0].id == self.task2_id
        assert done_tasks[0].status == Status.DONE
        
        # Test de filtrage avec le statut IN_PROGRESS
        in_progress_tasks = self.manager.get_tasks_by_status(Status.IN_PROGRESS)
        assert len(in_progress_tasks) == 1
        assert in_progress_tasks[0].id == self.task1_id

    def test_get_tasks_by_priority(self):
        """Test filtrage par priorité"""
        # Filtrage des tâches par priorité HIGH et vérification du résultat
        high_priority_tasks = self.manager.get_tasks_by_priority(Priority.HIGH)
        
        # Vérification que deux tâches ont la priorité HIGH (task1 et task4)
        assert len(high_priority_tasks) == 2
        high_task_ids = [task.id for task in high_priority_tasks]
        assert self.task1_id in high_task_ids
        assert self.task4_id in high_task_ids
        
        # Test de filtrage avec la priorité LOW
        low_priority_tasks = self.manager.get_tasks_by_priority(Priority.LOW)
        assert len(low_priority_tasks) == 1
        assert low_priority_tasks[0].id == self.task2_id
        
        # Test de filtrage avec la priorité MEDIUM
        medium_priority_tasks = self.manager.get_tasks_by_priority(Priority.MEDIUM)
        assert len(medium_priority_tasks) == 1
        assert medium_priority_tasks[0].id == self.task3_id

class TestTaskManagerPersistence:
    """Tests de sauvegarde/chargement avec mocks"""
    def setup_method(self):
        self.manager = TaskManager("test_tasks.json")
        # Création de tâches de test pour les tests de persistance
        self.task1_id = self.manager.add_task("Task 1", "Description 1", Priority.HIGH)
        self.task2_id = self.manager.add_task("Task 2", "Description 2", Priority.LOW)
        
        # Modification du statut d'une tâche pour diversifier les cas de test
        task1 = self.manager.get_task(self.task1_id)
        task1.mark_completed()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_to_file_success(self, mock_json_dump, mock_file):
        """Test sauvegarde réussie"""
        # Exécution de la sauvegarde des tâches
        self.manager.save_to_file()
        
        # Vérification que le fichier est ouvert en mode écriture avec le bon encodage
        mock_file.assert_called_once_with("test_tasks.json", 'w', encoding='utf-8')
        
        # Vérification que json.dump est appelé pour la sérialisation
        mock_json_dump.assert_called_once()
        
        # Vérification que les bonnes données sont passées à json.dump
        call_args = mock_json_dump.call_args
        tasks_data = call_args[0][0]  # Premier argument de json.dump
        assert len(tasks_data) == 2
        assert tasks_data[0]["title"] == "Task 1"
        assert tasks_data[1]["title"] == "Task 2"

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    @patch('json.load')
    def test_load_from_file_success(self, mock_json_load, mock_file):
        """Test chargement réussi"""
        # Configuration du mock pour retourner des données de test simulées
        test_data = [
            {
                "id": 1234567.0,
                "title": "Loaded Task",
                "description": "Loaded Description",
                "priority": "high",
                "status": "done",
                "created_at": "2024-01-01T12:00:00",
                "completed_at": "2024-01-01T13:00:00",
                "project_id": None
            }
        ]
        mock_json_load.return_value = test_data
        
        # Exécution du chargement depuis le fichier
        self.manager.load_from_file()
        
        # Vérification que les tâches ont été correctement chargées et désérialisées
        assert len(self.manager.tasks) == 1
        loaded_task = self.manager.tasks[0]
        assert loaded_task.title == "Loaded Task"
        assert loaded_task.description == "Loaded Description"
        assert loaded_task.priority == Priority.HIGH
        assert loaded_task.status == Status.DONE
        assert loaded_task.id == 1234567.0

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_from_nonexistent_file(self, mock_file):
        """Test chargement fichier inexistant"""
        # Tentative de chargement d'un fichier qui n'existe pas
        self.manager.load_from_file()
        
        # Vérification que l'opération ne lève pas d'exception
        # et que la liste des tâches reste vide (comportement attendu)
        assert len(self.manager.tasks) == 0

class TestTaskManagerAdditional:
    """Tests supplémentaires pour compléter la couverture"""
    def setup_method(self):
        """Fixture : gestionnaire de test"""
        self.manager = TaskManager("test_tasks.json")
        
    def test_delete_task_existing(self):
        """Test suppression d'une tâche existante"""
        task_id = self.manager.add_task("Task to delete", "Description", Priority.LOW)
        
        # Vérifier que la tâche existe
        assert len(self.manager.tasks) == 1
        
        # Supprimer la tâche
        result = self.manager.delete_task(task_id)
        
        # Vérifier que la suppression a réussi
        assert result is True
        assert len(self.manager.tasks) == 0
        
    def test_delete_task_nonexistent(self):
        """Test suppression d'une tâche inexistante"""
        # Essayer de supprimer une tâche qui n'existe pas
        result = self.manager.delete_task(999999)
        
        # Vérifier que la suppression a échoué
        assert result is False
        
    def test_get_statistics(self):
        """Test des statistiques"""
        # Ajouter des tâches avec différents statuts et priorités
        task1_id = self.manager.add_task("Task 1", "Desc 1", Priority.HIGH)
        task2_id = self.manager.add_task("Task 2", "Desc 2", Priority.LOW)
        task3_id = self.manager.add_task("Task 3", "Desc 3", Priority.MEDIUM)
        
        # Marquer une tâche comme terminée
        task1 = self.manager.get_task(task1_id)
        task1.mark_completed()
        
        # Modifier le statut d'une autre tâche
        task2 = self.manager.get_task(task2_id)
        task2.status = Status.IN_PROGRESS
        
        # Obtenir les statistiques
        stats = self.manager.get_statistics()
        
        # Vérifier les statistiques
        assert stats["total_tasks"] == 3
        assert stats["completed_tasks"] == 1
        
        # Vérifier la répartition par priorité
        assert stats["tasks_by_priority"]["high"] == 1
        assert stats["tasks_by_priority"]["low"] == 1
        assert stats["tasks_by_priority"]["medium"] == 1
        assert stats["tasks_by_priority"]["urgent"] == 0
        
        # Vérifier la répartition par statut
        assert stats["tasks_by_status"]["done"] == 1
        assert stats["tasks_by_status"]["in_progress"] == 1
        assert stats["tasks_by_status"]["todo"] == 1
        assert stats["tasks_by_status"]["cancelled"] == 0
        
    @patch('builtins.open', side_effect=IOError("Erreur d'écriture"))
    def test_save_to_file_error(self, mock_file):
        """Test gestion d'erreur lors de la sauvegarde"""
        self.manager.add_task("Test Task", "Description", Priority.MEDIUM)
        
        # Vérifier qu'une exception est levée
        with pytest.raises(Exception) as excinfo:
            self.manager.save_to_file()
        
        assert "Erreur lors de la sauvegarde" in str(excinfo.value)
        
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('json.load', side_effect=json.JSONDecodeError("msg", "doc", 0))
    def test_load_from_file_invalid_json(self, mock_json_load, mock_file):
        """Test chargement fichier JSON invalide"""
        # Vérifier qu'une exception est levée
        with pytest.raises(Exception) as excinfo:
            self.manager.load_from_file()
        
        assert "Erreur lors du chargement" in str(excinfo.value)