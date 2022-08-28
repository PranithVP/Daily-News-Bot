import tweepy
import praw
import os
from boto.s3.connection import S3Connection
from praw import Reddit
from tweepy import API

s3 = S3Connection(os.environ["TWITTER_KEY"],
                  os.environ["TWITTER_KEY_SECRET"],
                  os.environ["TWITTER_TOKEN"],
                  os.environ["TWITTER_TOKEN_SECRET"],
                  os.environ["REDDIT_USERNAME"],
                  os.environ["REDDIT_USER_AGENT"],
                  os.environ["REDDIT_PASSWORD"],
                  os.environ["REDDIT_CLIENT"],
                  os.environ["REDDIT_CLIENT_SECRET"])


def get_twitter_api_access() -> API:
    auth = tweepy.OAuthHandler(os.getenv("TWITTER_KEY"),
                               os.getenv("TWITTER_KEY_SECRET"))
    auth.set_access_token(os.getenv("TWITTER_TOKEN"),
                          os.getenv("TWITTER_TOKEN_SECRET"))
    api = tweepy.API(auth)
    return api


def get_reddit_api_access() -> Reddit:
    api = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"))
    return api
