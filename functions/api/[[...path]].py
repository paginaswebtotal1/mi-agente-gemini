from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY no configurada")

client = genai.Client(api_key=API_KEY)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        if not user_message:
            return jsonify({'error': 'Mensaje vacío'}), 400

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=user_message,
        )
        bot_response = response.text if response and response.text else "Lo siento, no pude generar una respuesta"
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()