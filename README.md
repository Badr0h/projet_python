# Location Simple

Une application de location entre particuliers développée avec Django.

## Fonctionnalités

- Inscription et authentification des utilisateurs
- Publication d'annonces avec photos
- Recherche et filtrage des annonces par catégorie
- Système de réservation
- Interface d'administration complète

## Prérequis

- Python 3.8+
- MySQL/MariaDB
- XAMPP (pour phpMyAdmin)

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone [URL_DU_DEPOT]
   cd location_simple
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   - Démarrer XAMPP et activer Apache et MySQL
   - Créer une base de données nommée `location_db` dans phpMyAdmin (http://localhost/phpmyadmin)

5. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

6. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

8. **Accéder à l'application**
   - Site web : http://127.0.0.1:8000/
   - Admin : http://127.0.0.1:8000/admin/

## Structure du projet

```
location_simple/
├── config/               # Configuration du projet
├── rental/               # Application principale
├── static/               # Fichiers statiques (CSS, JS, images)
├── templates/            # Templates HTML
├── media/                # Fichiers téléchargés
├── manage.py             # Script de gestion Django
└── requirements.txt      # Dépendances Python
```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.
