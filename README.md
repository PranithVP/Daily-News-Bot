# Daily-News-Bot
A python program that uses Reddit posts to formulate tweets on Twitter. 

The Reddit API is accessed via [PRAW](https://praw.readthedocs.io/en/stable/), and the Twitter API via [Tweepy](https://docs.tweepy.org/en/stable/). 

The program scrapes the top daily post from [r/news](https://www.reddit.com/r/news/) to construct a tweet. It then scans the article and generates 6 hashtags using keywords, as well as a summary by ordering the sentences on importance. The hashtags are included in the initial tweet, then a function is called to generate an image containing the summary (to bypass Twitter's character limit). After the initial tweet containing a title, article, and hashtags, the program replies to the tweet with the article summary.


# Hosting
[Heroku](https://www.heroku.com/) is used to host the bot on the cloud. 

It is scheduled to tweet at 1:00 AM, 5:00 AM, 9:00 AM, 1:00 PM, 5:00 PM, and 9:00 PM. 

A relevant tweet is retweeted at, 3:00 AM, 7:00 AM, 11:00 AM, 3:00 PM, 7:00 PM, and 11:00 PM.

A relevant tweet is liked at 12:00 AM, 2:00 AM, 4:00 AM, 6:00 AM, 8:00 AM, 10:00 AM, 12:00 PM, 2:00 PM, 4:00 PM, 6:00 PM, 8:00 PM, and 10:00 PM.
