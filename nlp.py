# nlp.py
# This file contains Natural Language Processing logic.
# It uses TextBlob to analyze sentiment of journal text.

from textblob import TextBlob


def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text.
    
    Polarity range:
    -1.0 (very negative) to +1.0 (very positive)
    
    Returns:
    - 'Positive'
    - 'Neutral'
    - 'Negative'
    """

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
