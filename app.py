from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return "✅ ESP32 Display Server is Online"

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# 🟢 Run on Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
