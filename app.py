import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Get API key and model name from environment variables
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-pro") # Default to gemini-pro

# Check for API key
if not api_key:
    # This will cause the function to fail cleanly if the key is not set
    raise RuntimeError("GEMINI_API_KEY environment variable not set.")

# Configure the generative AI model
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
except Exception as e:
    # This will help diagnose issues with the API key or model configuration
    raise RuntimeError(f"Failed to configure GenerativeModel: {e}")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Ensure the request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    try:
        response = model.generate_content(user_input)
        # Check if the response has text, handle cases where it might not
        if hasattr(response, 'text'):
            return jsonify({"response": response.text})
        else:
            # Log or handle cases where the response is not as expected
            return jsonify({"error": "Received an unexpected response from the model."}), 500
    except Exception as e:
        # More detailed error logging for debugging
        # In a real app, you'd use a proper logger
        error_message = f"An error occurred: {str(e)}"
        # Avoid exposing detailed internal errors to the client
        return jsonify({"error": "An internal error occurred."}), 500
