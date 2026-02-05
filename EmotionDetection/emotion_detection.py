"""
Emotion detection module.

This module sends user text to an emotion analysis API,
processes the response, and returns structured emotion scores
along with the dominant emotion.
"""

import requests


def emotion_detector(text_to_analyze):
    """
    Analyze emotions in the provided text.

    Args:
        text_to_analyze (str): The text input from the user.

    Returns:
        dict: A dictionary containing emotion scores and the dominant emotion.
              If analysis fails, dominant_emotion will be None.
    """

    # API endpoint for emotion detection
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"

    # Required headers for the API request
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # JSON payload sent to the API
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        # Send POST request to the API
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        # If API request fails, return safe fallback response
        if response.status_code != 200:
            return _empty_emotion_result()

        # Parse JSON response
        formatted_response = response.json()

        # Extract emotion predictions
        emotions = formatted_response["emotionPredictions"][0]["emotion"]

        # Get individual emotion scores
        anger = emotions["anger"]
        disgust = emotions["disgust"]
        fear = emotions["fear"]
        joy = emotions["joy"]
        sadness = emotions["sadness"]

        # Determine dominant emotion (highest score)
        emotion_scores = {
            "anger": anger,
            "disgust": disgust,
            "fear": fear,
            "joy": joy,
            "sadness": sadness,
        }
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        # Return structured result
        return {
            "anger": anger,
            "disgust": disgust,
            "fear": fear,
            "joy": joy,
            "sadness": sadness,
            "dominant_emotion": dominant_emotion,
        }

    except (requests.exceptions.RequestException, KeyError, ValueError):
        # Catch network issues or unexpected API response structure
        return _empty_emotion_result()


def _empty_emotion_result():
    """
    Return a default result when emotion detection fails.

    Returns:
        dict: Emotion scores set to None and no dominant emotion.
    """
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }
