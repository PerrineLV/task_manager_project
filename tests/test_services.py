import pytest
from unittest.mock import patch, Mock, mock_open
from datetime import datetime
from src.task_manager.services import EmailService, ReportService
from src.task_manager.task import Task, Priority

class TestEmailService:
    """Tests du service email avec mocks"""
    def setup_method(self):
        self.email_service = EmailService()

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_success(self, mock_smtp):
        """Test envoi rappel réussi avec mock SMTP"""
        # Configuration du mock SMTP pour simuler une connexion réussie
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Configuration des credentials pour l'authentification
        self.email_service.configure_credentials("test@example.com", "password")
        
        # Appel de la méthode à tester avec des paramètres valides
        result = self.email_service.send_task_reminder(
            "user@example.com", 
            "Test Task", 
            "2025-07-15"
        )
        
        # Vérification que l'email est considéré comme envoyé avec succès
        assert result is True
        # Vérification que la connexion SMTP a été établie
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        # Vérification que starttls() a été appelé pour le chiffrement
        mock_server.starttls.assert_called_once()

    def test_send_task_reminder_invalid_email(self):
        """Test envoi avec email invalide (sans @)"""
        # Test avec un email malformé qui ne contient pas de @
        with pytest.raises(ValueError, match="Format d'email invalide"):
            self.email_service.send_task_reminder(
                "invalid-email", 
                "Test Task", 
                "2025-07-15"
            )

    def test_send_task_reminder_invalid_email_no_domain(self):
        """Test envoi avec email invalide (sans domaine)"""
        # Test avec un email qui n'a pas de domaine valide
        with pytest.raises(ValueError, match="Format d'email invalide"):
            self.email_service.send_task_reminder(
                "user@", 
                "Test Task", 
                "2025-07-15"
            )

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_completion_notification_success(self, mock_smtp):
        """Test envoi notification de completion réussi"""
        # Configuration du mock SMTP pour simuler une connexion réussie
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Appel de la méthode pour envoyer une notification de completion
        result = self.email_service.send_completion_notification(
            "user@example.com", 
            "Test Task"
        )
        
        # Vérification que la notification est envoyée avec succès
        assert result is True
        # Vérification que la connexion SMTP a été établie
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        # Vérification que starttls() a été appelé pour le chiffrement
        mock_server.starttls.assert_called_once()

    @patch('src.task_manager.services.smtplib.SMTP')
    def test_send_task_reminder_smtp_error(self, mock_smtp):
        """Test gestion erreur SMTP lors de l'envoi"""
        # Configuration du mock pour lever une exception SMTP
        mock_smtp.side_effect = Exception("SMTP connection failed")
        
        # Appel de la méthode qui doit gérer l'exception
        result = self.email_service.send_task_reminder(
            "user@example.com", 
            "Test Task", 
            "2025-07-15"
        )
        
        # Vérification que l'erreur est gérée et retourne False
        assert result is False

class TestReportService:
    """Tests du service de rapports"""
    def setup_method(self):
        self.report_service = ReportService()
        # Création d'une liste de tâches de test avec différents états
        self.test_tasks = [
            Task("Tâche 1", "Description 1", Priority.HIGH),
            Task("Tâche 2", "Description 2", Priority.MEDIUM),
            Task("Tâche 3", "Description 3", Priority.LOW)
        ]
        # Marquage d'une tâche comme terminée pour les tests
        self.test_tasks[0].mark_completed()
        # Ajout d'un attribut completed pour compatibilité avec ReportService
        for task in self.test_tasks:
            task.completed = (task.status.value == "done")
        
        # Ajout d'attributs created_date pour les tests de rapport quotidien
        test_date = datetime(2025, 7, 11)
        for task in self.test_tasks:
            task.created_date = test_date

    def test_generate_daily_report_fixed_date(self):
        """Test génération rapport avec date fixe"""
        # Génération du rapport avec une date spécifique
        specific_date = datetime(2025, 7, 11)
        report = self.report_service.generate_daily_report(self.test_tasks, specific_date)
        
        # Vérification de la structure du rapport retourné
        assert "date" in report
        assert "total_tasks" in report
        assert "completed_tasks" in report
        assert "pending_tasks" in report
        assert "completion_rate" in report
        
        # Vérification des valeurs calculées
        assert report["date"] == "2025-07-11"
        assert report["total_tasks"] == 3
        assert report["completed_tasks"] == 1
        assert report["pending_tasks"] == 2
        assert report["completion_rate"] == 33.33

    def test_generate_daily_report_with_date_parameter(self):
        """Test génération rapport avec date spécifiée en paramètre"""
        # Génération du rapport avec une date spécifique
        specific_date = datetime(2025, 7, 11)
        report = self.report_service.generate_daily_report(self.test_tasks, specific_date)
        
        # Vérification que la date du rapport correspond à celle spécifiée
        assert report["date"] == "2025-07-11"
        assert report["total_tasks"] == 3

    def test_generate_daily_report_empty_tasks(self):
        """Test génération rapport avec liste vide"""
        # Génération du rapport avec une liste vide de tâches
        report = self.report_service.generate_daily_report([])
        
        # Vérification que le rapport gère correctement les listes vides
        assert report["total_tasks"] == 0
        assert report["completed_tasks"] == 0
        assert report["pending_tasks"] == 0
        assert report["completion_rate"] == 0

    @patch('builtins.open', new_callable=mock_open)
    def test_export_tasks_csv(self, mock_file):
        """Test export CSV avec mock du fichier"""
        # Configuration du nom de fichier pour l'export
        filename = "test_tasks.csv"
        
        # Appel de la méthode d'export avec les tâches de test
        result = self.report_service.export_tasks_csv(self.test_tasks, filename)
        
        # Vérification que l'export s'est terminé avec succès
        assert result is True
        # Vérification que le fichier a été ouvert en mode écriture
        mock_file.assert_called_once_with(filename, 'w', newline='', encoding='utf-8')
        # Vérification qu'il y a eu des écritures dans le fichier
        handle = mock_file.return_value.__enter__.return_value
        assert handle.write.called

    @patch('builtins.open', side_effect=PermissionError("Permission denied"))
    def test_export_tasks_csv_permission_error(self, mock_file):
        """Test export CSV avec erreur de permission"""
        # Test de gestion d'erreur de permission lors de l'écriture
        with pytest.raises(PermissionError, match="Permission refusée"):
            self.report_service.export_tasks_csv(self.test_tasks, "test.csv")

    @patch('builtins.open', side_effect=IOError("Disk full"))
    def test_export_tasks_csv_io_error(self, mock_file):
        """Test export CSV avec erreur d'entrée/sortie"""
        # Test de gestion d'erreur d'E/S lors de l'écriture
        with pytest.raises(IOError, match="Erreur d'écriture du fichier CSV"):
            self.report_service.export_tasks_csv(self.test_tasks, "test.csv")

    def test_generate_daily_report_current_date(self):
        """Test génération rapport avec date courante (datetime.now())"""
        # Génération du rapport sans spécifier de date (utilise datetime.now())
        report = self.report_service.generate_daily_report(self.test_tasks)
        
        # Vérification de la structure du rapport retourné
        assert "date" in report
        assert "total_tasks" in report
        assert "completed_tasks" in report
        assert "pending_tasks" in report
        assert "completion_rate" in report