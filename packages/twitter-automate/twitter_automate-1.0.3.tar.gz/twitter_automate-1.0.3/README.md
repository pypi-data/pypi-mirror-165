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
