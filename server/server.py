from flask import Flask, jsonify
import os

app = Flask(__name__)
# Fetch server ID from environment variable (set in docker)
SERVER_ID = os.environ.get("SERVER_ID", "Unknown")

@app.route("/home", methods=["GET"])
def server_home():
    return jsonify({
        "message": f"Hello from Server: {SERVER_ID}",
        "status": "successful"
    }), 200

@app.route("/")
def root():
    return "Server is running!"

@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return '', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
