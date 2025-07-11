# Makefile pour le projet task_manager

# Variables
PYTHON := python3
VENV := venv
VENV_BIN := $(VENV)/bin
PIP := $(VENV_BIN)/pip
PYTEST := $(VENV_BIN)/pytest
PYTHON_VENV := $(VENV_BIN)/python
SRC_DIR := src
TESTS_DIR := tests
COVERAGE_DIR := htmlcov
DIST_DIR := dist
BUILD_DIR := build

# Couleurs pour l'affichage
GREEN := \033[32m
RED := \033[31m
YELLOW := \033[33m
NC := \033[0m

.PHONY: help install test test-unit test-integration coverage clean lint all venv

# Affichage de l'aide
help:
	@echo "$(GREEN)Commandes disponibles:$(NC)"
	@echo "  $(YELLOW)venv$(NC)            - Créer l'environnement virtuel"
	@echo "  $(YELLOW)install$(NC)         - Installer les dépendances"
	@echo "  $(YELLOW)test$(NC)            - Lancer tous les tests"
	@echo "  $(YELLOW)test-unit$(NC)       - Lancer seulement les tests unitaires"
	@echo "  $(YELLOW)test-integration$(NC) - Lancer seulement les tests d'intégration"
	@echo "  $(YELLOW)coverage$(NC)        - Génerer un rapport de couverture HTML"
	@echo "  $(YELLOW)clean$(NC)           - Nettoyer les fichiers temporaires"
	@echo "  $(YELLOW)lint$(NC)            - Vérification syntaxique avec flake8"
	@echo "  $(YELLOW)all$(NC)             - Séquence complète (venv, install, lint, test, coverage)"

# Créer l'environnement virtuel
venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(GREEN)Création de l'environnement virtuel...$(NC)"; \
		$(PYTHON) -m venv $(VENV); \
		echo "$(GREEN)Environnement virtuel créé!$(NC)"; \
	else \
		echo "$(YELLOW)L'environnement virtuel existe déjà.$(NC)"; \
	fi

# Installer les dépendances
install: venv
	@echo "$(GREEN)Installation des dépendances...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install flake8 black isort
	@echo "$(GREEN)Installation terminée!$(NC)"

# Lancer tous les tests
test: venv
	@echo "$(GREEN)Lancement de tous les tests...$(NC)"
	$(PYTEST) $(TESTS_DIR) -v

# Lancer seulement les tests unitaires
test-unit: venv
	@echo "$(GREEN)Lancement des tests unitaires...$(NC)"
	$(PYTEST) $(TESTS_DIR) -v -m "unit"

# Lancer seulement les tests d'intégration
test-integration: venv
	@echo "$(GREEN)Lancement des tests d'intégration...$(NC)"
	$(PYTEST) $(TESTS_DIR) -v -m "integration"

# Générer un rapport de couverture HTML
coverage: venv
	@echo "$(GREEN)Génération du rapport de couverture...$(NC)"
	$(PYTEST) $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)Rapport de couverture généré dans $(COVERAGE_DIR)/$(NC)"

# Nettoyer les fichiers temporaires
clean:
	@echo "$(GREEN)Nettoyage des fichiers temporaires...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf $(COVERAGE_DIR)
	rm -rf $(DIST_DIR)
	rm -rf $(BUILD_DIR)
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf $(VENV)
	@echo "$(GREEN)Nettoyage terminé!$(NC)"

# Vérification syntaxique avec flake8
lint: venv
	@echo "$(GREEN)Vérification syntaxique...$(NC)"
	$(VENV_BIN)/flake8 $(SRC_DIR) $(TESTS_DIR) --max-line-length=88 --extend-ignore=E203,W503
	@echo "$(GREEN)Vérification terminée!$(NC)"

# Formatage du code
format: venv
	@echo "$(GREEN)Formatage du code...$(NC)"
	$(VENV_BIN)/black $(SRC_DIR) $(TESTS_DIR)
	$(VENV_BIN)/isort $(SRC_DIR) $(TESTS_DIR)
	@echo "$(GREEN)Formatage terminé!$(NC)"

# Séquence complète
all: venv install lint test coverage
	@echo "$(GREEN)Séquence complète terminée!$(NC)"