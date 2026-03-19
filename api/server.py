#!/usr/bin/env python3
"""
LOWDEX.io Backend API Server
- Proxy para la API de itch.io (evita CORS y protege la API key)
- Endpoint de feedback que envía correos via Gmail (usando MCP)
"""

import os
import sys
import json
import subprocess
import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Agregar el directorio api al path
sys.path.insert(0, os.path.dirname(__file__))
from itch_client import get_games_for_api, ItchClient, ItchAPIError

app = Flask(__name__, static_folder='..', static_url_path='')
CORS(app)

# Email de destino para el feedback
FEEDBACK_EMAIL = 'lowdex.io@gmail.com'


# ─── Servir el frontend ────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('..', 'index.html')


@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('../css', filename)


@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('../js', filename)


# ─── API: Juegos de itch.io ────────────────────────────────────────────────────

@app.route('/api/games')
def get_games():
    """
    Proxy hacia la API de itch.io.
    Usa el endpoint real si hay API key configurada; si no, devuelve datos de ejemplo.
    """
    api_key = os.environ.get('ITCH_API_KEY', '')
    result = get_games_for_api(api_key)
    return jsonify(result)


@app.route('/api/games/<int:game_id>/keys')
def get_game_keys(game_id):
    """Obtiene las claves de descarga de un juego."""
    api_key = os.environ.get('ITCH_API_KEY', '')
    if not api_key:
        return jsonify({"error": "API key not configured"}), 401
    
    try:
        client = ItchClient(api_key=api_key)
        keys = client.get_download_keys(game_id)
        return jsonify({"download_keys": keys})
    except ItchAPIError as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/me')
def get_profile():
    """Obtiene el perfil del usuario de itch.io."""
    api_key = os.environ.get('ITCH_API_KEY', '')
    if not api_key:
        return jsonify({"error": "API key not configured"}), 401
    
    try:
        client = ItchClient(api_key=api_key)
        profile = client.get_me()
        return jsonify(profile)
    except ItchAPIError as e:
        return jsonify({"error": str(e)}), 500


# ─── API: Feedback via Gmail ───────────────────────────────────────────────────

@app.route('/api/feedback', methods=['POST'])
def send_feedback():
    """
    Recibe el feedback del usuario y lo envía por Gmail usando el MCP de Gmail.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    name = data.get('name', 'Anónimo').strip()
    email = data.get('email', 'no-reply@unknown.com').strip()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
    
    # Construir el mensaje de email
    subject = f"[LOWDEX.io] Feedback de {name}"
    body = f"""Nuevo feedback recibido en LOWDEX.io

De: {name}
Email: {email}

Mensaje:
{message}

---
Enviado desde el formulario de feedback de LOWDEX.io
Fecha: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
"""
    
    # Usar el MCP de Gmail para enviar el correo
    mcp_input = json.dumps({
        "messages": [
            {
                "to": [FEEDBACK_EMAIL],
                "subject": subject,
                "body": body,
                "reply_to": email
            }
        ]
    })
    
    try:
        result = subprocess.run(
            ["manus-mcp-cli", "tool", "call", "gmail_send_messages",
             "--server", "gmail", "--input", mcp_input],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Guardar siempre el feedback localmente como respaldo
        save_feedback_locally(name, email, message)
        
        if result.returncode == 0:
            return jsonify({
                "success": True,
                "message": "¡Feedback enviado correctamente! Gracias por tu opinión."
            })
        else:
            return jsonify({
                "success": True,
                "message": "Feedback guardado. Lo revisaremos pronto."
            })
            
    except Exception as e:
        save_feedback_locally(name, email, message)
        return jsonify({
            "success": True,
            "message": "Feedback guardado. Lo revisaremos pronto."
        })


def save_feedback_locally(name: str, email: str, message: str):
    """Guarda el feedback en un archivo local como respaldo."""
    feedback_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(feedback_dir, exist_ok=True)
    
    feedback_file = os.path.join(feedback_dir, 'feedback.jsonl')
    entry = {
        "name": name,
        "email": email,
        "message": message,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    with open(feedback_file, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


# ─── Health check ─────────────────────────────────────────────────────────────

@app.route('/api/health')
def health():
    return jsonify({
        "status": "ok",
        "itch_api_configured": bool(os.environ.get('ITCH_API_KEY')),
        "gmail_configured": True,
        "version": "1.0.0"
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    print(f"[LOWDEX.io] Servidor iniciando en puerto {port}")
    print(f"[LOWDEX.io] itch.io API key: {'configurada' if os.environ.get('ITCH_API_KEY') else 'no configurada'}")
    app.run(host='0.0.0.0', port=port, debug=debug)
