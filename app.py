from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return "✅ ESP32 Display Server is Online"

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
