"""
Flask application factory.
Creates and configures the Flask application.
"""
from flask import Flask
from flask_cors import CORS
from app.config import get_config, Config
from app.utils import setup_logger, get_logger
from app.routes import main_bp, users_bp, ai_bp

logger = get_logger(__name__)


def create_app(config=None):
    """
    Create and configure Flask application.
    
    Args:
        config: Configuration object (optional)
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    
    # Load configuration
    if config is None:
        config = get_config()
    
    app.config.from_object(config)
    
    # Validate configuration
    try:
        Config.validate_config()
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    
    # Setup logging
    setup_logger(app)
    
    # Enable CORS for frontend
    CORS(app, resources={
        r"/users/*": {"origins": "*"},
        r"/ai/*": {"origins": "*"},
    })
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(ai_bp)
    
    # Error handlers
    register_error_handlers(app)
    
    logger.info(f"Flask application created (DEBUG={app.debug})")
    
    return app


def register_error_handlers(app):
    """Register global error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return {"error": "Resource not found"}, 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors"""
        return {"error": "Method not allowed"}, 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {str(error)}")
        return {"error": "Internal server error"}, 500
