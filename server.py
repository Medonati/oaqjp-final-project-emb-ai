"""
Flask server for Emotion Detection application.

This module handles HTTP routes, processes user input,
calls the emotion detection model, and returns formatted results.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

# Initialize Flask app
app = Flask("EmotionDetector")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    """
    Handle emotion detection requests from the frontend.

    Retrieves user text input, validates it, calls the emotion detector,
    and returns a formatted response.
    """
    # Get user input from query parameters
    text_to_analyze = request.args.get("textToAnalyze")

    # ---------- INPUT VALIDATION ----------

    # Check if input is empty or only spaces
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    # Check if input is purely numeric
    if text_to_analyze.strip().isdigit():
        return "Please enter a valid text!", 400

    # ---------- EMOTION DETECTION ----------

    result = emotion_detector(text_to_analyze)

    # If dominant emotion is None, the text was not valid for analysis
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    # ---------- RESPONSE FORMATTING ----------

    # Create response string with a line break before dominant emotion
    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}.<br>"
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return response_text


@app.route("/")
def render_index_page():
    """
    Render the main index page of the application.
    """
    return render_template("index.html")


if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
