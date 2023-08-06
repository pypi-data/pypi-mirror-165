# PACKAGE - KAI_AUOMATE

### **But**
Ce packages permet d'automatiser les tâches de like, partage et commentaire sur les réseaux sociaux tels que twitter et linkedIn.

### **Pour importer**
> from bot_linkedin.automate_linkedin import AutomateLinkedIn

### **Fonctions**
> 
- Pour LinkedIn
    > def linkedin_test_driver_manager_chrome(self): Allow to install chromedriver and out in PATH

    > def linkedin_get_ip(self): Allow to return proxy

    > def linkedin_create_session_crawl(self): Allow to add options of my driver

    > def linkedin_launch_page(self, link: str): Allow to create my driver

    > def linkedin_connect_account(self, url:str): Allow to connect on LinkedIn account with driver

    > def linkedin_get_last_publication(self): Allow to get a last publication. Here this function return a first 

    > def linkedin_get_publications(self): Allow to get a publication in list contains element de type object_selenium

    > def linkedin_like_post(self, post): Allow to like a post

    > def linkedin_share_post(self, post, text_share="Merci pour ce post"): Allow to share a post
                       
    > def linkedin_comment_post(self, post, text_comment="Très intéressant :)"): Allow to comment a post 

    > def linkedin_close_session(self):  Allow to close session create for the driver


### **Informations**
- Dans le dossier **dist/** nous avons notre package qui sera déplyer sur PyPi

- Utiliser la commande suivante **pip install -r requirements.txt** pour installer les librairies neccessaires

- Vous trouverez les différents class permettant d'automatiser les tâches sont dans le dossier **src/**

- Pour ce qui concerne la phase de tests j'utilise la librairie **pytest** pour tester mes class. Les fichiers contenant mes tests unitaires sont dans le dossier **tests/unit_test_xxx.py**. Pour exécuter les tests taper la commande **pytest unit_test_xxx.py**.

> NB: Soyez dans le répectoire tests/ pour exécuter

### **Informations supplémentaire**
Pour déployer le package utiliser twine en taper les commandes suivantes:

    - python setup.py sdist bdist

    - twine upload dist/*

        > Taper le username de votre compte PyPi

        > Taper le mot de passe de votre compte PyPi

### **Pour installer une fois déployer**
> pip install linkedin-bot