import json
import requests
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')    
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    
        response = {'status': 'API is working!', 'methods': ['POST']}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        # Handle CORS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract data from request
            user_message = data.get('message', '')
            api_key = data.get('apiKey', '')
            provider = data.get('provider', 'hkbu')
            model = data.get('model', 'gpt-4.1')
            system_prompt = data.get('systemPrompt', '')
            
            if not user_message or not api_key:
                response = {'error': 'Missing message or API key'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Call appropriate API based on provider
            if provider == 'hkbu':
                ai_response = call_hkbu_api(user_message, api_key, model, system_prompt)
            elif provider == 'openrouter':
                ai_response = call_openrouter_api(user_message, api_key, model, system_prompt)
            else:
                ai_response = "Error: Unsupported provider"
            
            response = {'response': ai_response}
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            error_response = {'error': f'Server error: {str(e)}'}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle preflight CORS request
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def call_hkbu_api(message, api_key, model, system_prompt):
    """Call HKBU GenAI API"""
    base_url = 'https://genai.hkbu.edu.hk/api/v0/rest'
    api_version = '2024-12-01-preview'
    
    # Build messages array
    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    messages.append({
        "role": "user", 
        "content": message
    })
    
    # Request payload
    payload = {
        "messages": messages,
        "max_tokens": 1000,
        "top_p": 0.9,
        "stream": False,
        "temperature": 0.7
    }
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key
    }
    
    try:
        url = f"{base_url}/deployments/{model}/chat/completions?api-version={api_version}"
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                return "Error: No response from HKBU API"
        else:
            return f"Error: HKBU API returned status {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return "Error: Request timeout. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error: Network error - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def call_openrouter_api(message, api_key, model, system_prompt):
    """Call OpenRouter API"""
    base_url = 'https://openrouter.ai/api/v1'
    
    # Build messages array
    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    
    messages.append({
        "role": "user",
        "content": message
    })
    
    # Request payload
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
        'HTTP-Referer': 'https://student-chat.vercel.app',
        'X-Title': 'HKBU Student Chatbot'
    }
    
    try:
        url = f"{base_url}/chat/completions"
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                return "Error: No response from OpenRouter API"
        else:
            return f"Error: OpenRouter API returned status {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return "Error: Request timeout. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error: Network error - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"