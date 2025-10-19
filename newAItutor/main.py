from flask import Flask, send_file, jsonify, request, Response
import os

app = Flask(__name__)

# Main route - serve the simple bot
@app.route('/')
def index():
    return send_file('bots/simpleBot.html')

@app.route('/bots/simpleBot.html')
def serve_simple_bot():
    return send_file('bots/simpleBot.html')

# Serve CSS files
@app.route('/bots/css/<filename>')
def serve_css(filename):
    return send_file(f'bots/css/{filename}')

# Serve JS files  
@app.route('/bots/js/<filename>')
def serve_js(filename):
    return send_file(f'bots/js/{filename}')

# Serve prompt files
@app.route('/prompts/<filename>')
def serve_prompts(filename):
    try:
        with open(f'prompts/{filename}', 'r', encoding='utf-8') as file:
            content = file.read()
        return Response(content, mimetype='text/plain')
    except FileNotFoundError:
        return f'Prompt file {filename} not found', 404
    except Exception as e:
        return f'Error: {str(e)}', 500

# Test API connection
@app.route('/api/test', methods=['POST'])
def test_api():
    try:
        data = request.get_json()
        api_key = data.get('apiKey', '')
        
        if len(api_key) > 10:
            return jsonify({'success': True, 'message': 'API key validated'})
        else:
            return jsonify({'error': 'Invalid API key format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Chat API
@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        message = data.get('message', '')
        api_key = data.get('apiKey', '')
        system_prompt = data.get('systemPrompt', '')
        
        # For testing - echo response
        response_text = f"Echo: {message}\n\n(This is a test response. In production, this would connect to HKBU GenAI API.)"
        
        return jsonify({'response': response_text, 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Simple AI Tutor")
    print("📍 Available at:")
    print("   http://localhost:5000/")
    print("   http://localhost:5000/bots/simpleBot.html")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Serve basic bot (main interface)
@app.route('/bots/basicBot.html')
def serve_basic_bot():
    return send_file('bots/basicBot.html')
