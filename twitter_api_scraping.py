from tweepy import API
from tweepy import Cursor
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np
import pasdas as pd

### TWITTTER CLIENT ###
class TwitterClient():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets.append(tweet)
        return tweets

#### TWITTER AUTHENTICATOR ####
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

###  TWITTER STREAMER ###
class TwitterStreamer():
    # Class for streaming and processing live tweets.    
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth =self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        
        # This line filters Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


### TWITTER STREAM LISTNER ###
class TwitterListener(StreamListener):
    #This is a basic listen class that just prnts received tweets to stdout

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        print(data)
        return True

    def on_error(self, status):
        if status == 420:
            # returns false on data method in case rate limit occurs.
            return False
        print(status)

if __name__ == "__main__":
    
    hash_tag_list = ["donald trump", "hillary clinton", "barack obama", "bernie sanders"]
    fetched_tweets_filename = "tweets.json"
    
    twitter_client =TwitterClient()
    print(twitter_client.get_user_timeline_tweets(1))
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

