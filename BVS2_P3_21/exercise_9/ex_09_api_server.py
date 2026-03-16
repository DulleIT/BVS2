from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

user_prompt = ""

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

@app.route('/set_prompt', methods=['GET'])
def set_prompt():
    global user_prompt
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "Missing prompt parameter"}), 400
    user_prompt = prompt
    return jsonify({"message": "Prompt set successfully"})

@app.route('/query', methods=['POST'])
def query():
    global user_prompt
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing message parameter"}), 400
    
    full_prompt = user_prompt + "\n" + data['message']

    try:
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json={"model": "phi", "prompt": full_prompt},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return jsonify({"answer": result.get("response", "")})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
