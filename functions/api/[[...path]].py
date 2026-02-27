from flask import Flask, request, jsonify
from google import genai
import os

# Crear app Flask
app = Flask(__name__)

# Configurar Gemini con API key de las variables de entorno
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY no configurada")

client = genai.Client(api_key=API_KEY)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para enviar mensajes a Gemini"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        # Llamar a Gemini
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=user_message,
        )
        
        # Procesar respuesta
        if response and hasattr(response, 'text') and response.text:
            bot_response = response.text
        else:
            bot_response = "Lo siento, no pude generar una respuesta"
        
        return jsonify({'response': bot_response})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Para entorno serverless
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()