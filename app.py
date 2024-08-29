from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OLLAMA_URL = 'http://localhost:11434/api/generate'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "model": "llama2",
        "prompt": user_input,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, headers=headers, json=data)
        if response.status_code != 200:
            return jsonify({"error": "Failed to connect to Ollama"}), 500

        try:
            response_data = response.json()
            generated_text = response_data['response']
            return jsonify({"response": generated_text})

        except ValueError as e:
            return jsonify({"error": "Invalid JSON response from Ollama", "details": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
