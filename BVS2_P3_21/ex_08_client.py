from flask import Flask, render_template, request, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Needed for flash messages

# Configuration for the API server
API_BASE_URL = 'http://localhost:5001'  # Assuming Docker container exposes port 5001

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = None
    error_message = None
    
    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        
        if user_input:
            try:
                # Send POST request to the API server's /query endpoint
                api_response = requests.post(
                    f'{API_BASE_URL}/query',
                    json={'message': user_input},
                    headers={'Content-Type': 'application/json'},
                    timeout=30  # 30 second timeout
                )
                
                if api_response.status_code == 200:
                    response_data = api_response.json()
                    response_text = response_data.get('answer', 'No answer received')
                else:
                    error_message = f"API Error ({api_response.status_code}): {api_response.text}"
                    
            except requests.exceptions.RequestException as e:
                error_message = f"Connection Error: {str(e)}"
            except json.JSONDecodeError:
                error_message = "Invalid JSON response from API"
        else:
            error_message = "Please enter some text"
    
    return render_template('index.html', 
                         response_text=response_text, 
                         error_message=error_message,
                         user_input=request.form.get('user_input', '') if request.method == 'POST' else '')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

