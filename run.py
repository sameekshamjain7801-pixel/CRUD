"""
Application entry point.
Run this file to start the Flask development server.
"""
import os
from app import create_app

if __name__ == "__main__":
    # Create application
    app = create_app()
    
    # Get configuration from environment
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    
    # Run application
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )
