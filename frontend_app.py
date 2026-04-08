# frontend_app.py
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# --- Configuration ---
# Replace with the actual URL of your backend service once deployed
BACKEND_SERVICE_URL = os.environ.get("BACKEND_SERVICE_URL", "http://localhost:8081")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Call the backend service for AI processing
        backend_response = requests.post(
            f"{BACKEND_SERVICE_URL}/process_message",
            json={"message": user_message}
        )
        backend_response.raise_for_status() # Raise an exception for HTTP errors
        ai_response = backend_response.json().get('response', 'Error: No AI response.')
        return jsonify({"response": ai_response})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Backend service error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

