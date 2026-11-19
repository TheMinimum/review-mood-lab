"""Sentiment model boundary. Replace this module when upgrading the model."""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MODEL_NAME = "VADER (vaderSentiment 3.3.2)"
MODEL_VERSION = "VADER 3.3.2"

_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> dict:
    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return {
        "label": label,
        "score": round(compound, 4),
        "positive": round(scores["pos"], 4),
        "negative": round(scores["neg"], 4),
        "neutral": round(scores["neu"], 4),
        "model": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "is_estimate": True,
    }
