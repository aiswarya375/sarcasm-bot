from flask import Flask, render_template, request
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        question = request.form.get("question")
        reply = generate_sarcastic_reply(question)
    return render_template("index.html", reply=reply)

def generate_sarcastic_reply(question):
    prompt = f"You are a witty and sarcastic chatbot. Give a short, funny, sarcastic reply in 1–2 sentences max. Never be serious.\nQuestion: {question}"
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    app.run(debug=True)
