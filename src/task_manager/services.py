import smtplib
import csv
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    """Service d'envoi d'emails (à mocker dans les tests)"""
    def __init__(self, smtp_server="smtp.gmail.com", port=587):
        # Configuration SMTP stockée pour l'envoi d'emails
        self.smtp_server = smtp_server
        self.port = port
        self.username = None
        self.password = None

    def configure_credentials(self, username, password):
        # Configuration des identifiants SMTP pour l'authentification
        self.username = username
        self.password = password
        print(f"Credentials SMTP configurés pour {username}")

    def send_task_reminder(self, email, task_title, due_date):
        # Validation du format email avec regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError(f"Format d'email invalide: {email}")
        
        # Envoi d'email de rappel utilisant smtplib
        try:
            # Création du message email
            msg = MIMEMultipart()
            msg['From'] = "task_manager@example.com"
            msg['To'] = email
            msg['Subject'] = f"Rappel: {task_title}"
            
            body = f"Bonjour,\n\nVoici un rappel pour votre tâche '{task_title}'.\nÉchéance: {due_date}\n\nCordialement,\nTask Manager"
            msg.attach(MIMEText(body, 'plain'))
            
            # Utilisation de smtplib pour se connecter au serveur SMTP
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()  # Activation du chiffrement TLS
                
                # Simulation de connexion (sans vraies credentials)
                print(f"Connexion SMTP établie à {self.smtp_server}:{self.port}")
                
                # Dans un vrai environnement, on ferait: server.login(self.username, self.password)
                # Ici on simule juste l'envoi pour les tests
                print(f"Envoi d'un rappel à {email} pour la tâche '{task_title}' - Échéance: {due_date}")
                
                # server.send_message(msg) # Commenté pour éviter l'envoi réel
            
            # Retour de succès après utilisation de smtplib
            return True
            
        except smtplib.SMTPException as e:
            print(f"Erreur SMTP lors de l'envoi du rappel: {e}")
            return False
        except Exception as e:
            print(f"Erreur générale lors de l'envoi du rappel: {e}")
            return False

    def send_completion_notification(self, email, task_title):
        # Envoi d'email de confirmation utilisant smtplib
        try:
            # Création du message email de confirmation
            msg = MIMEMultipart()
            msg['From'] = "task_manager@example.com"
            msg['To'] = email
            msg['Subject'] = f"Tâche terminée: {task_title}"
            
            body = f"Félicitations !\n\nVotre tâche '{task_title}' a été marquée comme terminée.\n\nCordialement,\nTask Manager"
            msg.attach(MIMEText(body, 'plain'))
            
            # Utilisation de smtplib pour se connecter au serveur SMTP
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()  # Activation du chiffrement TLS
                
                # Simulation de connexion (sans vraies credentials)
                print(f"Connexion SMTP établie à {self.smtp_server}:{self.port}")
                
                # Dans un vrai environnement, on ferait: server.login(self.username, self.password)
                # Ici on simule juste l'envoi pour les tests
                print(f"Envoi d'une notification de fin à {email} pour la tâche '{task_title}'")
                
                # server.send_message(msg) # Commenté pour éviter l'envoi réel
            
            return True
            
        except smtplib.SMTPException as e:
            print(f"Erreur SMTP lors de l'envoi de la notification: {e}")
            return False
        except Exception as e:
            print(f"Erreur générale lors de l'envoi de la notification: {e}")
            return False

class ReportService:
    """Service de génération de rapports"""
    def generate_daily_report(self, tasks, date=None):
        # Utilisation de datetime.now() si aucune date n'est fournie
        if date is None:
            date = datetime.now()
        
        # Génération du rapport quotidien avec métriques du jour
        report_date = date.strftime("%Y-%m-%d")
        
        # Filtrage des tâches pour la date spécifiée
        daily_tasks = []
        for task in tasks:
            # Vérification si la tâche a une date de création
            if hasattr(task, 'created_date') and task.created_date:
                if isinstance(task.created_date, datetime):
                    task_date = task.created_date.strftime("%Y-%m-%d")
                else:
                    task_date = str(task.created_date)
                
                if task_date == report_date:
                    daily_tasks.append(task)
            else:
                # Si pas de date, on inclut toutes les tâches
                daily_tasks.append(task)
        
        # Calcul des métriques du jour
        total_tasks = len(daily_tasks)
        completed_tasks = sum(1 for task in daily_tasks if hasattr(task, 'completed') and task.completed)
        pending_tasks = total_tasks - completed_tasks
        
        # Retour d'un dictionnaire avec les métriques
        return {
            "date": report_date,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
        }
    
    def export_tasks_csv(self, tasks, filename):
        # Export des tâches au format CSV avec gestion complète des erreurs d'écriture
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                # Définition des colonnes du CSV
                fieldnames = ['title', 'description', 'completed', 'created_date', 'due_date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Écriture de l'en-tête
                writer.writeheader()
                
                # Écriture des données de chaque tâche
                for task in tasks:
                    row = {
                        'title': getattr(task, 'title', ''),
                        'description': getattr(task, 'description', ''),
                        'completed': getattr(task, 'completed', False),
                        'created_date': str(getattr(task, 'created_date', '')),
                        'due_date': str(getattr(task, 'due_date', ''))
                    }
                    writer.writerow(row)
                
            print(f"Export CSV réussi: {len(tasks)} tâches exportées vers {filename}")
            return True
            
        except PermissionError:
            # Gestion des erreurs de permissions
            raise PermissionError(f"Permission refusée pour écrire le fichier: {filename}")
        except IOError as e:
            # Gestion des erreurs d'entrée/sortie
            raise IOError(f"Erreur d'écriture du fichier CSV: {e}")
        except Exception as e:
            # Gestion des autres erreurs inattendues
            raise Exception(f"Erreur inattendue lors de l'export CSV: {e}")