from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from GitHub Pages

DATA_FILE = "/data/tracker.json"

# ----------------- Helpers -----------------
def load_all():
    """Load tracker.json and normalize its structure."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except Exception:
                data = []

        # If old format (just an array of groups), wrap it
        if isinstance(data, list):
            data = {"groups": data, "users": {}}

        # Ensure both keys exist
        if "groups" not in data or not isinstance(data["groups"], list):
            data["groups"] = []
        if "users" not in data or not isinstance(data["users"], dict):
            data["users"] = {}

        return data
    else:
        # Start fresh if file doesn’t exist
        return {"groups": [], "users": {}}

def save_all(data):
    """Write tracker.json with proper structure."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ----------------- Routes -----------------

# Load all groups
@app.route("/load", methods=["GET"])
def load_groups():
    return jsonify(load_all()["groups"])

# Save groups
@app.route("/save", methods=["POST"])
def save_groups():
    data = load_all()
    data["groups"] = request.get_json(force=True)
    save_all(data)
    return jsonify({"status": "ok"})

# Load users
@app.route("/loadUsers", methods=["GET"])
def load_users():
    return jsonify(load_all()["users"])

# Save users
@app.route("/saveUsers", methods=["POST"])
def save_users():
    data = load_all()
    data["users"] = request.get_json(force=True)
    save_all(data)
    return jsonify({"status": "ok"})

# Root check
@app.route("/", methods=["GET"])
def root():
    return "BM Tracker backend is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
