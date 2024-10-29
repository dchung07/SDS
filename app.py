from flask import Flask, request, jsonify
from flask_cors import CORS
import state
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route("/get", methods=['GET'])
def get_json():
    try:
        logger.debug("GET request received at /get endpoint")
        result = state.get_state()
        logger.debug(f"State retrieved: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_json: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/get-history", methods=['GET'])
def get_history():
    try:
        args = request.args
        count = int(args.get("count", 1))
        logger.debug(f"GET request received at /get-history with count={count}")
        result = state.get_history(count)
        logger.debug(f"History retrieved: {result}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_history: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)