# Debug version of app.py
from flask import Flask, Response, request, jsonify
import state
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    print("Root endpoint called")
    return jsonify({"status": "Flask server is running"})

@app.route("/get", methods=['GET'])
def get_json():
    try:
        print("Get endpoint called")
        print("Current directory:", os.getcwd())
        print("Files in directory:", os.listdir())
        result = state.get_state()
        print("State result:", result)
        return jsonify(result)
    except Exception as e:
        print(f"Error in get_json: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    print("Current working directory:", os.getcwd())
    print("Files in directory:", os.listdir())
    app.run(host='127.0.0.1', port=5000, debug=True)