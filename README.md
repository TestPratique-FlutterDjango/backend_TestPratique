# API Publications - Django REST Framework

API REST pour la gestion de comptes utilisateurs, entreprises et publications.

## Fonctionnalités

### Authentification
- Inscription (compte privé ou professionnel)
- Connexion avec JWT
- Gestion du profil utilisateur
- Changement de mot de passe
- Déconnexion avec blacklist des tokens

### Comptes utilisateurs
- Compte privé : nom, email, adresse, mot de passe
- Compte pro : nom, email, nom entreprise, numéro CFE, adresse, mot de passe
- Mise à jour du profil

### Entreprises
- Ajout de plusieurs entreprises sur un compte
- CRUD complet des entreprises
- Activation/désactivation d'entreprises
- Liste des publications par entreprise

### Publications
- Création, modification et suppression de publications
- Statuts : Brouillon, Publié, Archivé
- Association à une entreprise (optionnel)
- Recherche avancée de publications
- Filtrage par statut, auteur, entreprise, tags, dates
- Compteur de vues
- Tags pour catégorisation

## Technologies

- Python 3.11+
- Django 5.0
- Django REST Framework 3.14
- PostgreSQL
- JWT (Simple JWT)
- drf-spectacular (documentation API)

## Installation

### 1. Cloner le repository

```bash
git clone <url-du-repo>
cd backend
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements/base.txt
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
# Modifier .env avec vos configurations
```

### 5. Créer la base de données PostgreSQL

```bash
createdb publications_db
```

### 6. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 8. Lancer le serveur

```bash
python manage.py runserver
```

L'API sera accessible sur : 'http://localhost:8000'

## Documentation de l'API

Une fois le serveur lancé :
- **Swagger UI** : http://localhost:8000/api/docs/
- **ReDoc** : http://localhost:8000/api/redoc/
- **Schema JSON** : http://localhost:8000/api/schema/

## Endpoints principaux

### Authentification
- 'POST /api/auth/register/' - Inscription
- 'POST /api/auth/login/' - Connexion
- 'POST /api/auth/logout/' - Déconnexion
- 'GET /api/auth/profile/' - Profil utilisateur
- 'PUT /api/auth/profile/' - Mise à jour du profil
- 'POST /api/auth/change-password/' - Changement de mot de passe
- 'POST /api/auth/token/refresh/' - Rafraîchir le token

### Entreprises
- 'GET /api/companies/' - Liste des entreprises
- 'POST /api/companies/' - Créer une entreprise
- 'GET /api/companies/{id}/' - Détail d'une entreprise
- 'PUT /api/companies/{id}/' - Mettre à jour une entreprise
- 'DELETE /api/companies/{id}/' - Supprimer une entreprise
- 'POST /api/companies/{id}/toggle_status/' - Activer/désactiver
- 'GET /api/companies/{id}/publications/' - Publications de l'entreprise

### Publications
- 'GET /api/publications/' - Liste des publications
- 'POST /api/publications/' - Créer une publication
- 'GET /api/publications/{id}/' - Détail d'une publication
- 'PUT /api/publications/{id}/' - Mettre à jour une publication
- 'DELETE /api/publications/{id}/' - Supprimer une publication
- 'GET /api/publications/my_publications/' - Mes publications
- 'GET /api/publications/search/' - Rechercher des publications
- 'POST /api/publications/{id}/publish/' - Publier
- 'POST /api/publications/{id}/archive/' - Archiver

## Exemples de requêtes

### Inscription (Compte privé)

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "address": "123 Main St",
    "account_type": "PRIVATE"
  }'
```

### Inscription (Compte professionnel)

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "pro@company.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Jane",
    "last_name": "Smith",
    "address": "456 Business Ave",
    "account_type": "PROFESSIONAL",
    "company_name": "My Company",
    "cfe_number": "CFE123456"
  }'
```

### Connexion

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Créer une publication

```bash
curl -X POST http://localhost:8000/api/publications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Ma première publication",
    "content": "Contenu de la publication",
    "status": "PUBLISHED",
    "tags": "tech, django, api"
  }'
```

### Rechercher des publications

```bash
curl -X GET "http://localhost:8000/api/publications/search/?q=django&status=PUBLISHED" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Tests

```bash
python manage.py test
```

## Déploiement

### Prérequis
- Service PostgreSQL (ElephantSQL, Neon, etc.)
- Plateforme de déploiement (Render, Railway, Fly.io)

### Variables d'environnement en production
- 'SECRET_KEY' : Clé secrète Django
- 'DATABASE_URL' : URL de connexion PostgreSQL
- 'ALLOWED_HOSTS' : Domaines autorisés
- 'CORS_ALLOWED_ORIGINS' : Origins CORS autorisées
- 'DEBUG=False'

## 📝 Structure du projet


backend/
    config/              # Configuration Django
    apps/
        accounts/       # Gestion utilisateurs
        companies/      # Gestion entreprises
        publications/   # Gestion publications
    core/               # Utilitaires communs
    requirements/       # Dépendances


## Auteur

DANGO NADEY Abdoul Fawaz

## Licence

MIT