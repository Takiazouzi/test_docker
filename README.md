# Enoncé

l'Application est composée de trois conteneurs Docker :
- `frontend` : Nginx sert la page de connexion et relaie `/api/` vers le backend.
- `backend` : API Python Flask qui vérifie les identifiants.
- `database` : MySQL 8.4 qui stocke les utilisateurs.
<img src=test.png>
Les trois conteneurs partagent le réseau Docker `app-network`. Seul le frontend publie un port sur la VM. Les données MySQL sont persistées par un bind mount `-v`.

## 1. Prérequis

- Une VM Linux avec Docker Engine installé et démarré.
- Accès Internet depuis la VM pour préparer l'environnement.

préparer l'environnement  :

```bash
git clone https://github.com/halekammoun/Test-Docker.git
```
```bash
cd  Test-Docker
```
```bash
bash env.sh
```
[Ouvrir l'exercice interactif](exercice.html)
# Questions
### 1. Créer le Dockerfile du backend

<label>
  <input type="checkbox">
- [ ] Le backend doit être construit à partir d'une image Python officielle nommé python:3.12-slim
</label>

- [ ] Définit les variables d'environnement PYTHONDONTWRITEBYTECODE=1 et PYTHONUNBUFFERED=1
- [ ] Définir le répertoire de travail /app.
- [ ] Copier le fichier requirements.txt.
- [ ] Installer les dépendances Python en utilisant la commande pip install --no-cache-dir -r requirements.txt
- [ ] Copier le code de l'application.
- [ ] Documenter le port d'écoute du backend qui est 5000.
- [ ] Définir la commande de démarrage.
### 2. Construire l'image du backend
- [ ] Construisez l'image sous le nom login-backend et le tag 1.0.

- [ ] Vérifiez ensuite sa présence dans la liste des images locales.
### 3. Construire l'image du Frontend
- [ ] Construisez ensuite l'image nommée login-frontend:1.0.
### 4. Création du réseau Docker
- [ ] Créez un réseau Docker nommé app-network.
- [ ] Vérifiez que le réseau existe
### 5. Préparer un répertoire de stockage host pour la base de données.
- [ ] Créez le répertoire suivant sur la VM :
/opt/docker-login/mysql-data
Ce répertoire doit stocker les données de MySQL en dehors du cycle de vie du conteneur.
### 6. Démarrage du Conteneur Database
Démarrez ensuite un conteneur
- [ ] nommé database
- [ ] en mode `detached`
- [ ] à partir de l'image officielle `mysql:8.4`.
- [ ] Le réseau app-network.
- [ ] Persite les données du conteneur /var/lib/mysql en utilisant le montage `-v`, faits le nécessaire pour que le conteneur aura la permission de partager les données sous le réperoire hote.
Configurez aussi la base de donnée tel que:
- [ ] Le mot de passe administrateur MySQL: MYSQL_ROOT_PASSWORD='RootPass_ChangeMe123!'
- [ ] Le nom de la base de données login_db: MYSQL_DATABASE='login_db'
- [ ] Le nom d'utilisateur applicatif appuser: MYSQL_USER='appuser'
- [ ] Le mot de passe de cet utilisateur: MYSQL_PASSWORD='AppPass_ChangeMe123!'
Aprés le démarrage attends que MySQL soit prêt :
```bash
docker logs -f database
```
Quand le journal indique que MySQL est prêt, quittez l'affichage avec `Ctrl+C`. Cela ne stoppe pas le conteneur.

### 7. Démarrage du Conteneur Backend
- [ ] Lancez le conteneur backend à partir de l'image login-backend:1.0.
Il doit :
- [ ] Être connecté au réseau app-network.
- [ ] Être en mode `detached`
- [ ] Recevoir les variables d'environnement nécessaires qui sont:
DB_HOST='database'  
DB_PORT='3306'  
DB_NAME='login_db'  
DB_USER='appuser'   
DB_PASSWORD='AppPass_ChangeMe123!'  
ADMIN_USERNAME='student'   
ADMIN_PASSWORD='DockerLab123!'  
### 8. Démarrage du conteneur Frontend
- [ ] Démarrez le conteneur frontend à partir de l'image login-frontend:1.0.
Il doit :
- [ ] Être connecté au réseau app-network.
- [ ] Être accessible sur l'hote en 8080; **HINT**: inspecte le fichier frontend/nginx.conf et frontend/Dockerfile pour connaitre le port du conteneur.
### 9 Tester la connexion 
- [ ] Ouvrez l'application dans le navigateurde la VM.
- [ ] entrer ces Identifiants de démonstration :
Utilisateur : `student`
Mot de passe : `DockerLab123!`