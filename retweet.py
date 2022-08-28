import auth
import random


def retweet_relevant_tweet() -> None:
    twitter_api = auth.get_twitter_api_access()
    following = twitter_api.get_friend_ids()
    random_user_index = random.randint(0, len(following) - 1)
    tweet_list = twitter_api.user_timeline(count=1,
                                           user_id=following[random_user_index],
                                           include_rts=False,
                                           tweet_mode='extended')
    for tweet in tweet_list:
        twitter_api.retweet(tweet.id)


retweeted = False
while not retweeted:
    try:
        retweet_relevant_tweet()
        retweeted = True
    except:
        continue

