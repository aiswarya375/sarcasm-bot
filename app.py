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

SIMPLE_REPLIES = [
    "Oh brilliant question — I almost forgot how curious humans are.",
    "Let me drop everything and fix your life.",
    "Amazing. Another question from the collection of questions.",
    "Sure, because clearly the internet owes you an answer.",
    "Wow, groundbreaking stuff. Please continue."
]

def generate_sarcastic_reply(question):
    # If Gemini/OpenAI configured, try to generate; otherwise fallback.
    if HAS_GENAI:
        try:
            prompt = (
                "You are a witty and sarcastic chatbot. Give a short, funny, "
                "sarcastic reply in 1–2 sentences max. Never be serious.\n"
                f"Question: {question}"
            )
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text:
                return text
        except Exception:
            pass
    # fallback: random canned reply with slight variation
    return random.choice(SIMPLE_REPLIES)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400
    reply = generate_sarcastic_reply(question)
    # Burn meter value (60-100) — how savage the reply is
    burn = random.randint(60, 100)
    return jsonify({"reply": reply, "burn": burn})

if __name__ == "__main__":
    app.run(debug=True)
