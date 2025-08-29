# app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'status': 'HKBU Student Chatbot API is running!', 'endpoints': ['/api/chat', '/api/test']})

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        # Handle preflight CORS request
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        data = request.json
        user_message = data.get('message', '')
        api_key = data.get('apiKey', '')
        provider = data.get('provider', 'hkbu')
        model = data.get('model', 'gpt-4.1')
        system_prompt = data.get('systemPrompt', '')
        
        if not api_key:
            return jsonify({'error': 'No API key provided'}), 400
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Route to appropriate API based on provider
        if provider == 'hkbu':
            response_text = call_hkbu_api(user_message, api_key, model, system_prompt)
        elif provider == 'openrouter':
            response_text = call_openrouter_api(user_message, api_key, model, system_prompt)
        else:
            return jsonify({'error': 'Unsupported provider'}), 400
        
        return jsonify({
            'response': response_text
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400

@app.route('/api/test', methods=['POST'])
def test_connection():
    try:
        data = request.json
        api_key = data.get('apiKey', '')
        provider = data.get('provider', 'hkbu')
        model = data.get('model', 'gpt-4.1')
        
        if not api_key:
            return jsonify({'error': 'No API key provided'}), 400
        
        # Test with a simple message
        if provider == 'hkbu':
            response = call_hkbu_api('Hello, this is a test.', api_key, model, 'You are a helpful assistant.')
        elif provider == 'openrouter':
            response = call_openrouter_api('Hello, this is a test.', api_key, model, 'You are a helpful assistant.')
        else:
            return jsonify({'error': 'Unsupported provider'}), 400
        
        return jsonify({
            'response': f'Connection successful! Response: {response[:50]}...'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 400

# ADD THIS NEW ROUTE HERE:
@app.route('/frontend')
def serve_frontend():
    return send_file('index.html')

def call_hkbu_api(message, api_key, model, system_prompt):
    """Call HKBU GenAI API"""
    base_url = "https://genai.hkbu.edu.hk/api/v0/rest"
    api_version = "2024-12-01-preview"
    url = f"{base_url}/deployments/{model}/chat/completions?api-version={api_version}"
    
    # Prepare messages
    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    payload = {
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.9,
        "stream": False
    }
    
    try:
        print(f"HKBU API Request to: {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"HKBU Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception("Invalid response format from HKBU API")
        elif response.status_code == 401:
            raise Exception("HKBU API: Invalid API key or access denied")
        elif response.status_code == 404:
            raise Exception(f"HKBU API: Model '{model}' not found")
        else:
            error_text = response.text
            raise Exception(f"HKBU API Error {response.status_code}: {error_text}")
            
    except requests.exceptions.Timeout:
        raise Exception("HKBU API: Request timeout")
    except requests.exceptions.RequestException as e:
        raise Exception(f"HKBU API: Network error - {str(e)}")

def call_openrouter_api(message, api_key, model, system_prompt):
    """Call OpenRouter API"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Prepare messages
    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": message})
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://smartlessons.hkbu.tech",
        "X-Title": "HKBU Student Chatbot"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    try:
        print(f"OpenRouter API Request to: {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"OpenRouter Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception("Invalid response format from OpenRouter API")
        elif response.status_code == 401:
            raise Exception("OpenRouter API: Invalid API key")
        elif response.status_code == 402:
            raise Exception("OpenRouter API: Insufficient credits")
        else:
            error_text = response.text
            raise Exception(f"OpenRouter API Error {response.status_code}: {error_text}")
            
    except requests.exceptions.Timeout:
        raise Exception("OpenRouter API: Request timeout")
    except requests.exceptions.RequestException as e:
        raise Exception(f"OpenRouter API: Network error - {str(e)}")

if __name__ == '__main__':
    print("🚀 Starting HKBU Student Chatbot Server...")
    print("📝 Available endpoints:")
    print("   GET  / - API status")
    print("   GET  /frontend - Web interface")
    print("   POST /api/chat - Chat with AI")
    print("   POST /api/test - Test API connection")
    print("\n🔧 Make sure to:")
    print("   1. Install: pip install flask flask-cors requests")
    print("   2. Get HKBU API key: https://genai.hkbu.edu.hk/settings/api-docs")
    print("   3. Get OpenRouter key: https://openrouter.ai/keys")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)