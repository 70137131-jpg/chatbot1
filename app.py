import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Load .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

if not api_key:
    raise RuntimeError(
        "Missing GEMINI_API_KEY. Add it to your .env file or export it in the shell."
    )

if not model_name:
    model_name = "gemini-pro" # Default to gemini-pro if not set

print("Environment configured successfully.")

# Initialize the generative model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name)

print(f"Using model: {model_name}")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    try:
        response = model.generate_content(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
