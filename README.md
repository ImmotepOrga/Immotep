# DOCKERAZATIOOOOOOON !!

- How to do maaan ?
- Easy ! First step : go to the root of the project. 
- Okaaay
- Second step : write the following command "docker-compose build"
- Yes yes yes ! Lots of lines appear !
- Normaaaal boy, next write this command "docker-compose up"
- It's done ! Next ?
- That's all hehehe 😎


# Setup

- Quelques commandes utiles pour installer correctement ce projet
- A lancer à la racine


## Sélectionner le bon environnement
Développement
> .env décommenter le bloc PRODUCTION
Production
> .env décommenter le bloc DEVELOPPEMENT

## Créer un environnement virtuel

Windows 

```bash
python -m venv env
env/Scripts/activate
```
Mac 

```bash
python -m venv env
source env/bin/activate
```
## Installer les dépendances / packages

```bash
pip install -r requirements.txt
```
## Configurer les variables d'environnements

- Créer un fichier ".env" dans le dossier "/project" (au même niveau que le fichier settings.py) et copiez le contenu suivant
- Adaptez les lignes selon votre environnement (nom de la base, nom d'utilisateur, mot de passe)

```bash
DATABASE_NAME=database_name
DATABASE_USER=user_name
DATABASE_PASSWORD=password
```

## Migration BDD

Créer une migration (Nommez-la par clarté)
```bash
python manage.py makemigrations --name nom_exemple
```
Migrer les changements vers la BDD
```bash
python manage.py migrate
```
## Lancer le serveur

```bash
python manage.py runserver
```
