from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Variable zum Speichern des Prompts (anfangs leer)
stored_prompt = ""

@app.route('/set_prompt', methods=['GET'])
def set_prompt():
    global stored_prompt
    prompt = request.args.get('prompt')
    if prompt is None:
        return "Missing prompt parameter", 400
    stored_prompt = prompt
    return f"Prompt gesetzt: {stored_prompt}"

@app.route('/query', methods=['POST'])
def query():
    global stored_prompt
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing message parameter'}), 400
    
    message = data['message']
    # Kombiniere den gespeicherten Prompt und die neue Nachricht
    combined_prompt = f"{stored_prompt}\n{message}"
    
    try:
        # Rufe ollama über subprocess auf - der Prompt wird über stdin übergeben
        result = subprocess.run(
            ['ollama', 'run', 'phi'],
            input=combined_prompt,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        answer = result.stdout.strip()
        return jsonify({'answer': answer})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'ollama run failed: {e.stderr}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
