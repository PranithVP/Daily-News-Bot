import io
import auth
import textwrap
from typing import Any
from PIL import Image, ImageDraw, ImageFont
from newspaper import Article
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


def summarize(post: Any) -> str:
    # Input text - to summarize
    article = Article(post.url)
    article.download()
    article.parse()
    text = article.text

    # Tokenizing the text
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)

    # Creating a frequency table to keep the score of each word
    freq_table = dict()
    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1

    # Creating a dictionary to keep the score of each sentence
    sentences = sent_tokenize(text)
    sentence_value = dict()
    for sentence in sentences:
        for word, freq in freq_table.items():
            if word in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq
                else:
                    sentence_value[sentence] = freq
    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]

    # Average value of a sentence from the original text
    average = int(sum_values / len(sentence_value))

    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        if (sentence in sentence_value) and (
                sentence_value[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary.strip()


def reply_image(text):
    wrapped_text = textwrap.wrap(text, width=67)
    w, h = (755, len(wrapped_text) * 45)
    font = ImageFont.truetype('georgia.ttf', 22)
    img = Image.new("RGBA", (w, h), "white")
    draw = ImageDraw.Draw(img)
    for i in range(len(wrapped_text)):
        draw.multiline_text((35, 40 * (i + 1)), font=font,
                            text=wrapped_text[i], fill=(0, 0, 0))
    file = io.BytesIO()
    img.save(file, 'PNG')
    file.seek(0)
    twitter_api = auth.get_twitter_api_access()
    user = twitter_api.user_timeline(screen_name="Daily_News_Bot", count=1,
                                     include_rts=False, tweet_mode='extended')
    for tweet in user:
        twitter_api.update_status_with_media(
            in_reply_to_status_id=tweet.id, filename="Description", file=file,
            status="Didn't read the article? No worries, here's a summary:")

