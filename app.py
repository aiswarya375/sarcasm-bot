from flask import Flask, render_template, request, jsonify
import random
import os

try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

app = Flask(__name__)

SIMPLE_REPLIES = {
    "mild": [
        "Oh, that's a cute question.",
        "Well, aren't you curious today?",
        "Sure, I'll humor you with an answer."
    ],
    "savage": [
        "Oh brilliant question — I almost forgot how curious humans are.",
        "Let me drop everything and fix your life.",
        "Amazing. Another question from the collection of questions."
    ],
    "extra": [
        "Wow, groundbreaking stuff. Please continue.",
        "Sure, because clearly the internet owes you an answer.",
        "I'm overwhelmed with your brilliance, really."
    ]
}

def generate_sarcastic_reply(question, style="savage"):
    if HAS_GENAI:
        try:
            prompt = (
                f"You are a witty and sarcastic chatbot with a {style} tone. "
                "Give a short, funny, sarcastic reply in 1–2 sentences max. Never be serious.\n"
                f"Question: {question}"
            )
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text:
                return text
        except Exception:
            pass
    return random.choice(SIMPLE_REPLIES.get(style, SIMPLE_REPLIES["savage"]))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    question = data.get("question", "").strip()
    style = data.get("style", "savage")
    if not question:
        return jsonify({"error": "No question provided"}), 400
    reply = generate_sarcastic_reply(question, style)
    burn = random.randint(60, 100)
    return jsonify({"reply": reply, "burn": burn})

if __name__ == "__main__":
    app.run(debug=True)
