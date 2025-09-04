from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from GitHub Pages

DATA_FILE = "/data/tracker.json"
USERS_FILE = "users.json"

# --- Tracker routes ---
@app.route("/load", methods=["GET"])
def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    return jsonify(data)

@app.route("/save", methods=["POST"])
def save():
    try:
        data = request.get_json(force=True)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

# --- User routes ---
def load_users_file():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        # default accounts if no users.json exists yet
        return [
            { "user": "admin", "pass": "admin123", "role": "admin" },
            { "user": "user",  "pass": "user123",  "role": "user" },
            { "user": "dev",   "pass": "dev123",   "role": "dev" }
        ]

def save_users_file(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/loadUsers", methods=["GET"])
def load_users():
    return jsonify(load_users_file())

@app.route("/saveUsers", methods=["POST"])
def save_users():
    try:
        data = request.get_json(force=True)
        save_users_file(data)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

# --- Root check ---
@app.route("/", methods=["GET"])
def root():
    return "BM Tracker backend is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
