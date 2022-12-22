# Daily News Bot
A python program that uses Reddit posts to formulate tweets on Twitter. 

The Reddit API is accessed via , and the Twitter API via [Tweepy](https://docs.tweepy.org/en/stable/). 

The program scrapes the top daily post from [r/news](https://www.reddit.com/r/news/) to construct a tweet. It then scans the article and generates 6 hashtags using keywords, as well as a summary by ordering the sentences on importance. The hashtags are included in the initial tweet, then a function is called to generate an image containing the summary (to bypass Twitter's character limit). After the initial tweet containing a title, article, and hashtags, the program replies to the tweet with the article summary.

A link to the bot's twitter account can be found [here](https://twitter.com/Daily_News_Bot).
