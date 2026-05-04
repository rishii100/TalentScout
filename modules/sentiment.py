"""
Sentiment Analysis Module (Bonus)
=================================
Uses Gemini to classify the emotional tone of candidate messages.
Results are displayed in the UI and stored in the session data.
"""

from core.llm import generate_single_response

# Sentiment categories and their display properties
SENTIMENT_MAP = {
    "positive": {"emoji": "😊", "color": "#4CAF50", "label": "Positive"},
    "neutral": {"emoji": "😐", "color": "#9E9E9E", "label": "Neutral"},
    "negative": {"emoji": "😟", "color": "#FF9800", "label": "Concerned"},
    "frustrated": {"emoji": "😤", "color": "#F44336", "label": "Frustrated"},
    "excited": {"emoji": "🤩", "color": "#2196F3", "label": "Excited"},
    "confused": {"emoji": "😕", "color": "#FF9800", "label": "Confused"},
}

_SENTIMENT_SYSTEM = """You are a sentiment classifier. Analyze the emotional tone of \
candidate messages in a job screening conversation. \
Respond with ONLY one word from: positive, neutral, negative, frustrated, excited, confused."""


def analyze_sentiment(message: str) -> dict:
    """
    Analyze the sentiment of a candidate's message.

    Parameters
    ----------
    message : str
        The candidate's message text.

    Returns
    -------
    dict
        Sentiment info with keys: sentiment, emoji, color, label.
    """
    if not message or len(message.strip()) < 3:
        return SENTIMENT_MAP["neutral"] | {"sentiment": "neutral"}

    prompt = f"Classify the sentiment of this job candidate's message:\n\"{message}\""
    result = generate_single_response(prompt, _SENTIMENT_SYSTEM).lower().strip()

    # Match to known sentiments
    for key in SENTIMENT_MAP:
        if key in result:
            return SENTIMENT_MAP[key] | {"sentiment": key}

    # Default to neutral
    return SENTIMENT_MAP["neutral"] | {"sentiment": "neutral"}
