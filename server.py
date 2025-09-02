from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = "tracker.json"

@app.route("/load", methods=["GET"])
def load():
    """Return the latest tracker data as JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    return jsonify(data)

@app.route("/save", methods=["POST"])
def save():
    """Accept JSON from client and overwrite tracker.json"""
    try:
        data = request.get_json(force=True)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

@app.route("/", methods=["GET"])
def root():
    return "BM Tracker backend is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
