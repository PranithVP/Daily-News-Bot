# Import libraries
import auth
import random


def like_latest_tweet(username: str):
    """ Like a user's latest tweet.
    """
    # Get Twitter API access
    twitter_api = auth.get_twitter_api_access()
    user = twitter_api.user_timeline(screen_name=username, count=1,
                                     include_rts=False, tweet_mode='extended')
    # Like the latest tweet by the user
    for tweet in user:
        twitter_api.create_favorite(tweet.id)


def like_relevant_tweet():
    """ Like a tweet relevant to current news.
    """
    # Get Twitter API access
    twitter_api = auth.get_twitter_api_access()
    following = twitter_api.get_friend_ids()

    # Choose a random user from following 
    random_user_index = random.randint(0, len(following) - 1)

    # Like the user's latest tweet
    tweet_list = twitter_api.user_timeline(count=1,
                                           user_id=following[random_user_index],
                                           include_rts=False,
                                           tweet_mode='extended')
    for tweet in tweet_list:
        twitter_api.create_favorite(tweet.id)


# Like a random relevant post
liked = False
while not liked:
    try:
        like_relevant_tweet()
        liked = True
    except:
        continue
