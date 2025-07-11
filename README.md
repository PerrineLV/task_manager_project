# Task Manager Project

Un gestionnaire de tâches complet développé en Python, permettant de créer, organiser et gérer des tâches avec différentes priorités et statuts.

## 🚀 Fonctionnalités

- **Gestion des tâches** : Créer, modifier, supprimer et organiser des tâches
- **Système de priorités** : LOW, MEDIUM, HIGH, URGENT
- **Statuts de tâches** : TODO, IN_PROGRESS, DONE, CANCELLED
- **Persistance des données** : Sauvegarde et chargement au format JSON
- **Services intégrés** :
  - Service d'envoi d'emails (rappels et notifications)
  - Service de génération de rapports (quotidiens et export CSV)
- **Statistiques** : Analyse complète des tâches par statut et priorité
- **Tests complets** : Couverture de tests unitaires et d'intégration

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

## 🛠️ Installation

### 1. Cloner le projet

```bash
git clone <url-du-repository>
cd task_manager_project
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate     # Sur Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Alternative : Utiliser le Makefile

```bash
# Créer l'environnement virtuel et installer les dépendances
make install

# Voir toutes les commandes disponibles
make help
```

## 🎯 Utilisation

### Utilisation basique

```python
from src.task_manager.manager import TaskManager
from src.task_manager.task import Priority, Status

# Créer un gestionnaire de tâches
manager = TaskManager("mes_taches.json")

# Ajouter une tâche
task_id = manager.add_task(
    "Préparer la présentation",
    "Créer les slides pour la réunion client",
    Priority.HIGH
)

# Récupérer une tâche
task = manager.get_task(task_id)
print(f"Tâche: {task.title} - Priorité: {task.priority.value}")

# Marquer une tâche comme terminée
task.mark_completed()

# Sauvegarder les tâches
manager.save_to_file()

# Charger les tâches depuis un fichier
manager.load_from_file()
```

### Filtrage et recherche

```python
# Obtenir les tâches par statut
taches_todo = manager.get_tasks_by_status(Status.TODO)
taches_terminees = manager.get_tasks_by_status(Status.DONE)

# Obtenir les tâches par priorité
taches_urgentes = manager.get_tasks_by_priority(Priority.URGENT)
taches_importantes = manager.get_tasks_by_priority(Priority.HIGH)

# Obtenir les statistiques
stats = manager.get_statistics()
print(f"Total: {stats['total_tasks']}")
print(f"Terminées: {stats['completed_tasks']}")
print(f"Par priorité: {stats['tasks_by_priority']}")
```

### Services avancés

```python
from src.task_manager.services import EmailService, ReportService

# Service d'email
email_service = EmailService()
email_service.configure_credentials("user@example.com", "password")

# Envoyer un rappel
email_service.send_task_reminder(
    "destinataire@example.com",
    "Tâche importante",
    "2024-12-31"
)

# Service de rapports
report_service = ReportService()

# Générer un rapport quotidien
rapport = report_service.generate_daily_report(manager.tasks)
print(f"Tâches créées aujourd'hui: {rapport['total_tasks']}")

# Exporter en CSV
report_service.export_tasks_csv(manager.tasks, "export_taches.csv")
```

### Exemple complet

Consultez le fichier `demo.py` pour un exemple complet d'utilisation :

```bash
python demo.py
```

## 🧪 Tests

### Lancer tous les tests

```bash
# Avec pytest
pytest

# Avec make
make test
```

### Tests avec couverture

```bash
# Générer le rapport de couverture
make coverage

# Voir le rapport HTML
make coverage-html
```

### Types de tests disponibles

- **Tests unitaires** : `make test-unit`
- **Tests d'intégration** : `make test-integration`
- **Tests de performance** : `make test-performance`

## 📊 Structure du projet

```
task_manager_project/
├── src/
│   └── task_manager/
│       ├── __init__.py
│       ├── task.py          # Classe Task et énumérations
│       ├── manager.py       # Gestionnaire principal
│       └── services.py      # Services email et rapports
├── tests/
│   ├── __init__.py
│   ├── test_task.py         # Tests de la classe Task
│   ├── test_manager.py      # Tests du gestionnaire
│   ├── test_services.py     # Tests des services
│   └── fixtures/            # Données de test
├── demo.py                  # Démonstration d'utilisation
├── requirements.txt         # Dépendances Python
├── Makefile                 # Commandes automatisées
└── README.md               # Documentation
```

## 🔧 Configuration

### Fichier de configuration des tâches

Les tâches sont sauvegardées au format JSON. Exemple :

```json
[
  {
    "id": 1640995200.0,
    "title": "Exemple de tâche",
    "description": "Description de la tâche",
    "priority": "high",
    "status": "todo",
    "created_at": "2024-01-01T10:00:00",
    "completed_at": null,
    "project_id": null
  }
]
```

### Variables d'environnement

Pour le service d'email, vous pouvez configurer :

```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export EMAIL_USERNAME="votre-email@gmail.com"
export EMAIL_PASSWORD="votre-mot-de-passe"
```

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commitez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

### Standards de code

- Utilisez `black` pour le formatage du code
- Respectez les conventions PEP 8
- Ajoutez des tests pour toute nouvelle fonctionnalité
- Documentez vos fonctions avec des docstrings

## 📈 Métriques de qualité

- **Couverture de tests** : > 95%
- **Linting** : Conforme aux standards Python
- **Documentation** : Toutes les fonctions publiques documentées

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :

1. Consultez la documentation
2. Vérifiez les issues existantes
3. Créez une nouvelle issue si nécessaire

## 🔄 Changelog

### Version 1.0.0
- Implémentation initiale du gestionnaire de tâches
- Système de priorités et statuts
- Services d'email et de rapports
- Tests complets avec couverture > 95%