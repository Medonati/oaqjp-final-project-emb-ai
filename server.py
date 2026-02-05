from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("EmotionDetector")

@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    textToAnalyze = request.args.get("textToAnalyze")

    result = emotion_detector(textToAnalyze)

    # Check if dominant_emotion is None → invalid text
    if result['dominant_emotion'] is None:
        return "Invalid text! Please try again!", 400

    # Format response with line break before dominant emotion
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
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
