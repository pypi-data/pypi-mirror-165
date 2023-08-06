# KAI_AUTOMATE_TWITTER -- APPLICATION
"""
    This class is used to automate tasks on
    TWITTER social networks.
    This class will allow
        - LIKE
        - RETWEETER
        - COMMENT
"""

import sys
from pprint import pprint
pprint(sys.path)
# Libraty to automate TWITTER
import tweepy

#  Library native of python
from datetime import date

class AutomateTwitter:
    credentials = {}
    
    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str, pseudo_twitter: str):
        """ Description:
                This function is a constructor of my class.
                For having credentials, you should create your twiiter developper account on this link :
                https://developer.twitter.com/en/portal/

            Params:
                :param self:
            
                :param consumer_key:str: it's consumer_key of application you create on twitter developper account
            
                :param consumer_secret:str:  it's consumer_secret: of application you create on twitter developper account
            
                :param access_token:str: it's access_token of application you create on twitter developper account
            
                :param access_token_secret:str: it's access_token_secret of application you create on twitter developper account
            
                :param pseudo_twitter:str: it's your pseudo of twitter account 
        """    
        self.credentials['consumer_key'] =  consumer_key
        self.credentials['consumer_secret'] =  consumer_secret
        self.credentials['access_token'] =  access_token
        self.credentials['access_token_secret'] =  access_token_secret
        self.credentials['pseudo_twitter'] =  pseudo_twitter
        
        print('Object create')
    
    def twitter_auth_api(self):
        """ Description
                This function allow to authentificate on Twitter API
            
            Params:
                :param self:
    
            Returns:
                api:object
        """    
        auth = tweepy.OAuthHandler(self.credentials['consumer_key'], self.credentials['consumer_secret'])
        auth.set_access_token(self.credentials['access_token'],self.credentials['access_token_secret'])
        api = tweepy.API(auth)
        print('API connect')
        return api
    
    def twitter_auth_client(self):
        """ Description
                This function allow to authentificate on Twitter Client
            
            Params:
                :param self:
    
            Returns:
                client:object
        """   
        client = tweepy.Client(
            consumer_key = self.credentials['consumer_key'], consumer_secret= self.credentials['consumer_secret'],
            access_token= self.credentials['access_token'], access_token_secret= self.credentials['access_token_secret']
        )
        print('Client connect')
        return client   
    
    def twitter_get_last_post(self, user_api: twitter_auth_api, pseudo_twitter: str) -> dict:
        """ Description
                This function return a dictionary contain id of last tweet and date creation
            
            Params:
                :param self:
            
                :param user_api:twitter_auth_api: credentials of Twitter API
            
                :param pseudo_twitter:str: pseudo of twitter account  
    
            Returns:
                last_tweet_data:dict
        """ 
        try:
            tweets_user_target = user_api.user_timeline(screen_name = pseudo_twitter, count=1)
            
            last_tweet_data = {}
            last_tweet_data['id_tweet'] = str(tweets_user_target[0].id)
            last_tweet_data['created_tweet'] = tweets_user_target[0].created_at.date()
            
            return last_tweet_data
        except Exception as e:
            print("I can not send last post. Read error ", e, "\n")
            raise
        
    def twitter_get_posts(self, user_api: twitter_auth_api, pseudo_twitter: str, nb_tweet: int) -> list:
        """ Description:
                This function return last tweets in function value of variable 'nb_tweet'

            Params:
                :param self:
            
                :param user_api:twitter_auth_api: credentials of Twitter API
            
                :param pseudo_twitter:str: pseudo of twitter account  
            
                :param nb_tweet:int: number of tweet to retrieve
            
            Returns:
                data_on_tweets_user_target:list
        """
        try:
            tweets_user_target = user_api.user_timeline(screen_name = pseudo_twitter, count=nb_tweet)
            
            data_on_tweets_user_target = []
            
            for  tweet in tweets_user_target:
                tweet_data = {}
                tweet_data['id_tweet'] = str(tweet.id)
                tweet_data['created_tweet'] = tweet.created_at.date()
                data_on_tweets_user_target.append(tweet_data)
                
            return data_on_tweets_user_target     
        except Exception as e:
            print("I can not create list posts. Read error ", e, "\n")
            raise
        
    def twitter_automate_like (self, user_client: twitter_auth_client, id_post: str):
        """ Description
                This function allow to like a tweet
            Params
                :param self:
            
                :param user_client:twitter_auth_client: credentials of Twitter API
            
                :param id_post:str: id of tweet 
            
            Return:
                object
        """    
        try:
            return user_client.like(
                tweet_id = str(id_post),
                user_auth = True
            )
        except Exception as e:
            print("You can not like this tweet. Read error ", e, "\n")
            raise
        
    def twitter_automate_retweet(self, user_client: twitter_auth_client, id_post: str):
        """ Description
                This function allow to retweet a tweet
            Params
                :param self:
            
                :param user_client:twitter_auth_client: credentials of Twitter API
            
                :param id_post:str: id of tweet 
            
            Return:
                object
        """ 
        try:
            return user_client.retweet(
                tweet_id = str(id_post),
                user_auth = True
            )
        except Exception as e:
            print("You can not retweet this tweet. Read error ", e, "\n")
            raise

    def twitter_automate_comment(self, user_client: twitter_auth_client, id_post: str, text_comment: str):  
        """ Description
                This function allow to comment a tweet
            Params
                :param self:
            
                :param user_client:twitter_auth_client: credentials of Twitter API
            
                :param id_post:str: id of tweet 
            
            Return:
                object
        """
        try: 
            return user_client.create_tweet(
                text = text_comment,
                in_reply_to_tweet_id = str(id_post)
            )
        except Exception as e:
            print('This comment is already used for this tweet', e, "\n")
            raise
        
