# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'chat.html')

@app.route('/test-api', methods=['POST'])
def test_api():
    try:
        data = request.json
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'success': False, 'error': 'No API key provided'}), 400
        
        # Test with a simple message
        response = call_hkbu_api([{'role': 'user', 'content': 'Hi'}], api_key, 'gpt-4.1')
        
        return jsonify({
            'success': True,
            'message': 'API key is valid',
            'response': response[:100] + '...' if len(response) > 100 else response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        api_key = data.get('api_key')
        model = data.get('model', 'gpt-4.1')
        system_prompt = data.get('system_prompt', '')
        conversation_history = data.get('conversation_history', [])
        
        if not api_key:
            return jsonify({'success': False, 'error': 'No API key provided'}), 400
        
        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400
        
        # Prepare messages
        messages = []
        if system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        # Call HKBU API
        response = call_hkbu_api(messages, api_key, model)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def call_hkbu_api(messages, api_key, model):
    endpoints_to_try = [
        f"https://genai.hkbu.edu.hk/api/v0/rest/deployments/{model}/chat/completions",
        "https://genai.hkbu.edu.hk/api/chat/completions",
        "https://genai.hkbu.edu.hk/chat/completions"
    ]
    
    headers_to_try = [
        {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        {"Content-Type": "application/json", "api-key": api_key},
        {"Content-Type": "application/json", "X-API-Key": api_key},
        {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}
    ]
    
    payload = {
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 1,
        "stream": False
    }
    
    api_versions = ["2024-12-01-preview", "2024-06-01", "2023-12-01-preview"]
    
    last_error = None
    
    for endpoint in endpoints_to_try:
        for headers in headers_to_try:
            for version in api_versions + [None]:
                try:
                    url = f"{endpoint}?api-version={version}" if version else endpoint
                    
                    print(f"Trying: {url} with auth method: {list(headers.keys())}")
                    
                    response = requests.post(url, headers=headers, json=payload, timeout=30)
                    
                    print(f"Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        if "choices" in result and len(result["choices"]) > 0:
                            return result["choices"][0]["message"]["content"]
                        else:
                            raise Exception("Invalid response format")
                    
                    elif response.status_code == 401:
                        last_error = Exception("Invalid API key")
                        continue
                        
                    elif response.status_code == 404:
                        last_error = Exception("Endpoint not found")
                        break
                        
                    else:
                        error_text = response.text
                        print(f"Error response: {error_text}")
                        last_error = Exception(f"API Error {response.status_code}: {error_text}")
                        
                except requests.exceptions.RequestException as e:
                    last_error = Exception(f"Request failed: {str(e)}")
                    print(f"Request exception: {e}")
                    continue
    
    if last_error:
        raise last_error
    else:
        raise Exception("All API endpoints failed. The HKBU GenAI service might be temporarily unavailable.")

if __name__ == '__main__':
    print("Starting HKBU GenAI Chatbot Server...")
    print("Make sure to:")
    print("1. Install requirements: pip install flask flask-cors requests")
    print("2. Place chat.html in the same directory")
    print("3. Get your API key from https://genai.hkbu.edu.hk/settings/api-docs")
    app.run(debug=True, port=5000)