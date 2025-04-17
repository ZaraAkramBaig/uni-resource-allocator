from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        logger.error(f"Validation error: {error.messages}")
        return jsonify({"error": "Validation error", "messages": error.messages}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        logger.error(f"Resource not found: {error}")
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        logger.error(f"HTTP error {error.code}: {error.description}")
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500