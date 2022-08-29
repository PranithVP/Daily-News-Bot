# Import packages
import auth
import nltk
import reply
import like
import sys
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
    # Get Reddit API access
    reddit_api = auth.get_reddit_api_access()
    news_subreddit = reddit_api.subreddit("news")
    posts = news_subreddit.top(limit=post_number, time_filter="day")
    count = 1

    # Return the correct post according to post_number
    for item in posts:
        if count == post_number:
            return item
        count += 1


def get_hashtag_list(url: str, amount: int) -> List[str]:
    """ Generate a list of hashtags using the url with the specified amount of
    hashtags.
    """
    # Extract the text from the article
    article = Article(url)
    article.download()
    article.parse()

    # Extract keywords from text and make frequency dictionary
    rake = Rake()
    rake.extract_keywords_from_text(article.text)
    freq_dict = rake.get_word_frequency_distribution()

    # Return a list of the necessary amount of hashtags
    words = [key for key in freq_dict if (freq_dict[key] > 2) and
             key.isalpha() and len(key) > 1]
    article_text = word_tokenize('\n'.join(word + " " for word in words))
    words = [word for word in article_text if word not in stopwords.words()]
    if len(words) >= amount:
        return words[:amount]


def get_previous_tweets(username: str) -> List[str]:
    """ Return a list of a user's previous article titles.
    """
    # Get Twitter API access
    api = auth.get_twitter_api_access()
    user = api.user_timeline(screen_name=username, count=16,
                             include_rts=False, tweet_mode='extended')
    
    # Merge tweets into string
    tweets_merged = ''
    for status in user:
        tweets_merged += status.full_text
    tweets_list = tweets_merged.split('\n')[::2]
    titles = []

    # Add titles from tweets to titles list, return title list
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


# Download missing packages
nltk.download('stopwords')
nltk.download('punkt')

# Declare variables
tweeted = False
number = 1

# Get Twitter API access
twitter_api = auth.get_twitter_api_access()

# Search for reddit posts until post is tweeted
while not tweeted:
    # Try tweeting unless error is raised
    try:
        print("Attempting to tweet")
        # Get previous tweet list and top reddit post
        previous_tweets = get_previous_tweets("Daily_News_Bot")
        post = get_reddit_post(number)
        hashtags_list = get_hashtag_list(post.url, 6)
        
        # Create hashtag list, summary, restrictions
        unique = post.title not in previous_tweets
        hashtags_exist = hashtags_list is not None
        text = reply.summarize(post)
        image, lines = reply.make_image(text)
        restrictions = ["apnews", "eastidahonews"]
        not_restricted = True
        for item in restrictions:
            not_restricted = item not in post.url and not_restricted

        # Check for restrictions, empty hashtag list, duplications, and summary
        if hashtags_exist and unique and not_restricted and 4 < lines < 23:
            hashtags = "".join("#" + word + " " for word in hashtags_list)
            content = post.title + "\n" + hashtags + "\n" + post.url
            twitter_api.update_status(content)
            tweeted = True
            like.like_latest_tweet("Daily_News_Bot")
            reply.reply_image(image)
        else:
            print("Criteria not met (" + number + ")")
            number += 1
            if number > 15:
                exit()
    # If any error is raised, iterate to next reddit post
    except:
        print("Error (" + number + ")")
        number += 1
        if number > 15:
            exit()
