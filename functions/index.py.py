from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    return send_from_directory(templates_dir, 'index.html')

def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()