import auth
import nltk
import reply
import like
from typing import Any, List
from newspaper import Article
from nltk import word_tokenize
from nltk.corpus import stopwords
from rake_nltk import Rake


def get_reddit_post(post_number: int) -> Any:
    """ Find the nth most upvoted reddit post in the past 24 hours where n is
    the post_number.

    Precondition: post_number >= 1
    """
    reddit_api = auth.reddit_api_access()
    news_subreddit = reddit_api.subreddit("news")
    posts = news_subreddit.top(limit=post_number, time_filter="day")
    count = 1
    for item in posts:
        if count == post_number:
            return item
        count += 1


def get_hashtag_list(url: str, amount: int) -> List[str]:
    """ Generate a list of hashtags using the url with the specified amount of
    hashtags.
    """
    article = Article(url)
    article.download()
    article.parse()
    rake = Rake()
    rake.extract_keywords_from_text(article.text)
    freq_dict = rake.get_word_frequency_distribution()
    words = [key for key in freq_dict if (freq_dict[key] > 2) and
             key.isalpha() and len(key) > 1]
    text = '\n'.join(word + " " for word in words)
    text = word_tokenize(text)
    words = [word for word in text if word not in stopwords.words()]
    if len(words) >= amount:
        return words[:amount]


def get_previous_tweets() -> List[str]:
    """ Return a list of @Daily_News_Bot's previous article titles.
    """
    api = auth.twitter_api_access()
    user = api.user_timeline(screen_name='Daily_News_Bot', count=16,
                             include_rts=False, tweet_mode='extended')
    tweets_merged = ''
    for status in user:
        tweets_merged += status.full_text
    tweets_list = tweets_merged.split('\n')[::2]
    titles = []
    # Add titles from tweets to titles list
    for i in range(len(tweets_list)):
        # Ignore multiple urls + TLDR text
        if tweets_list[i][:5] == 'https' and tweets_list[i][23:27] == "Didn":
            titles.append(tweets_list[i][101:])
        # Ignore twitter url
        elif tweets_list[i][:5] == 'https':
            titles.append(tweets_list[i][23:])
        # Ignore TLDR text + twitter URL
        else:
            titles.append(tweets_list[i][78:])
    return titles


def tweet(content: str) -> None:
    """ Post a tweet using the provided text.
    """
    twitter_api = auth.twitter_api_access()
    twitter_api.update_status(content)


# Download missing packages
nltk.download('stopwords')
nltk.download('punkt')

# Declare variables
tweeted = False
number = 1

# Search for reddit posts until post is tweeted
while not tweeted:
    # Try tweeting unless error is raised
    try:
        # Get previous tweet list and top reddit post
        previous_tweets = get_previous_tweets()
        post = get_reddit_post(number)
        hashtags_list = get_hashtag_list(post.url, 6)
        # Tweet post if hashtag list is valid and article is not a duplicate
        unique = post.title not in previous_tweets
        hashtags_exist = hashtags_list is not None
        restrictions = ["https://apnews"]
        if hashtags_exist and unique and post.url[:14] not in restrictions:
            hashtags = "".join("#" + word + " " for word in hashtags_list)
            tweet(post.title + "\n" + hashtags + "\n" + post.url)
            tweeted = True
            like.like_latest_tweet()
            text = reply.summarize(post)
            reply.reply_image(text)
        else:
            number += 1
    # If error is raised, iterate to next reddit post
    except:
        number += 1
