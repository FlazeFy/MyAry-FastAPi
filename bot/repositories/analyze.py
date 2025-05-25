from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_mood(text: str) -> tuple[str, float]:
    result = sentiment_pipeline(text)[0]
    label = result['label']
    score = result['score']

    if label == "POSITIVE" and score >= 0.7:
        mood = "happy 😊"
    else:
        mood = "not happy 😞"

    return mood, score