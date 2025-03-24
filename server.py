from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Bolt API startup')

# Deep Seek API configuration
DEEPSEEK_API_URL = "https://api.deepseek.ai/v1/chat/completions"  # Updated endpoint
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

if not DEEPSEEK_API_KEY:
    app.logger.error('DEEPSEEK_API_KEY not found in environment variables')
    raise ValueError('DEEPSEEK_API_KEY must be set')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_response():
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided"}), 400

        prompt = data['prompt']
        app.logger.info(f'Generating response for prompt: {prompt[:50]}...')
        
        # Call Deep Seek API
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant specializing in software development and technical tasks."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            app.logger.info(f'Making request to Deep Seek API with headers: {headers}')
            app.logger.info(f'Request payload: {payload}')
            
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
            app.logger.info(f'Deep Seek API Response Status: {response.status_code}')
            app.logger.info(f'Deep Seek API Response Headers: {response.headers}')
            app.logger.info(f'Deep Seek API Response Body: {response.text}')
            
            response.raise_for_status()
            result = response.json()
            
            # Check if the response has the expected structure
            if 'choices' not in result or not result['choices']:
                raise ValueError('Invalid response format from Deep Seek API')
                
            app.logger.info('Successfully generated response')
            return jsonify({
                "choices": [{
                    "message": {
                        "content": result['choices'][0]['message']['content']
                    }
                }]
            })
            
        except requests.exceptions.RequestException as e:
            app.logger.error(f'Deep Seek API request failed: {str(e)}')
            if hasattr(response, 'status_code'):
                if response.status_code == 401:
                    return jsonify({"error": "Invalid API key"}), 401
                elif response.status_code == 429:
                    return jsonify({"error": "Rate limit exceeded"}), 429
            return jsonify({"error": f"API request failed: {str(e)}"}), 503
    
    except Exception as e:
        app.logger.error(f'Unexpected error: {str(e)}')
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        return jsonify({
            "status": "healthy",
            "api_key_configured": bool(DEEPSEEK_API_KEY)
        })
    except Exception as e:
        app.logger.error(f'Health check failed: {str(e)}')
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)