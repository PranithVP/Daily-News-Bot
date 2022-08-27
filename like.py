import auth
import random


def like_latest_tweet():
    """ Like @Daily_News_Bot's latest tweet.
    """
    twitter_api = auth.twitter_api_access()
    user = twitter_api.user_timeline(screen_name="Daily_News_Bot", count=1,
                                     include_rts=False, tweet_mode='extended')
    for tweet in user:
        twitter_api.create_favorite(tweet.id)


def like_relevant_tweet():
    """ Like a tweet relevant to current news.
    """
    twitter_api = auth.twitter_api_access()
    following = twitter_api.get_friend_ids()
    random_user_index = random.randint(0, len(following) - 1)
    tweet_list = twitter_api.user_timeline(count=1,
                                           user_id=following[random_user_index],
                                           include_rts=False,
                                           tweet_mode='extended')
    for tweet in tweet_list:
        twitter_api.create_favorite(tweet.id)


like_relevant_tweet()
