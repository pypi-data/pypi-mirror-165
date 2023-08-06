# PACKAGE - TWITTER-AUTOMATE

### **But**
Ce packages permet d'automatiser les tâches de like, partage et commentaire sur Twitter.

### **Pour importer**

    from bot_twitter import automate_twitter as at

### **Fonctions**

- **twitter_auth_api(self)**: 

    This function allow to authentificate on Twitter API

- **twitter_auth_client(self)**: 

    This function allow to authentificate on Twitter Client

- **twitter_get_last_post(self, user_api: twitter_auth_api, pseudo_twitter: str)**: 

    This function return a dictionary contain id of last tweet and date creation

- **twitter_get_posts(self, user_api: twitter_auth_api, pseudo_twitter: str, nb_tweet: int)**: 

    This function return last tweets in function value of variable 'nb_tweet'

- **twitter_like (self, user_client: twitter_auth_client, id_post: str)**: 

    This function allow to like a tweet

- **twitter_retweet(self, user_client: twitter_auth_client, id_post: str)**: 

    This function allow to retweet a tweet

- **twitter_comment(self, user_client: twitter_auth_client, id_post: str, text_comment: str)**: 

    This function allow to comment a tweet   

### **Informations**
- Dans le dossier **dist/** nous avons notre package qui sera déplyer sur PyPi

- Utiliser la commande suivante **pip install -r requirements.txt** pour installer les librairies neccessaires

- Vous trouverez les différents class permettant d'automatiser les tâches sont dans le dossier **src/**

- Dans le fichier **MANIFEST.in** il est important de préciser le dossier contenant la class gérant l'automatisation. Donc le dossier
**bot_twitter/**. 

> NB: Si le dossier n'est pas appelé, le package ne fonctionnera pas une fois déployé

- Pour ce qui concerne la phase de tests j'utilise la librairie **pytest** pour tester mes class. Les fichiers contenant mes tests unitaires sont dans le dossier **tests/unit_test_xxx.py**. Pour exécuter les tests taper la commande **pytest unit_test_xxx.py**.

> NB: Soyez dans le répectoire tests/ pour exécuter

### **Informations supplémentaire**
Pour déployer le package utiliser twine en taper les commandes suivantes:

- python setup.py sdist bdist

- twine upload dist/*

    > Taper le username de votre compte PyPi

    > Taper le mot de passe de votre compte PyPi

### **Pour installer une fois déployer**
> pip install twitter-automate