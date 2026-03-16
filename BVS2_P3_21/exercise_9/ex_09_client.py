from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

API_SERVER_URL = "http://api_server:5003"  # Docker Compose DNS-Name

HTML = """
<!doctype html>
<title>Chatbot Client</title>
<h1>Chatbot Client</h1>

<form id="promptForm">
  Set prompt: <input type="text" name="prompt" id="promptInput" required>
  <button type="submit">Set Prompt</button>
</form>

<form id="queryForm" style="margin-top:20px;">
  Send message: <input type="text" name="message" id="messageInput" required>
  <button type="submit">Send</button>
</form>

<div id="response" style="margin-top:20px; font-weight:bold;"></div>

<script>
document.getElementById('promptForm').onsubmit = async function(e) {
  e.preventDefault();
  const prompt = document.getElementById('promptInput').value;
  const res = await fetch(`/set_prompt?prompt=${encodeURIComponent(prompt)}`);
  const json = await res.json();
  alert(json.message || json.error);
}

document.getElementById('queryForm').onsubmit = async function(e) {
  e.preventDefault();
  const message = document.getElementById('messageInput').value;
  const res = await fetch('/query', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message})
  });
  const json = await res.json();
  document.getElementById('response').textContent = json.answer || json.error;
}
</script>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/set_prompt')
def set_prompt():
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "Missing prompt parameter"}), 400
    # Forward to API Server
    res = requests.get(f"{API_SERVER_URL}/set_prompt", params={"prompt": prompt})
    return jsonify(res.json())

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing message parameter"}), 400
    res = requests.post(f"{API_SERVER_URL}/query", json={"message": data['message']})
    return jsonify(res.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
