"""
Logging utility for the application.
"""
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(app):
    """
    Configure application logging.
    
    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.mkdir("logs")
    
    # Configure file handler with rotation
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # Set logging format
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    
    # Set log level based on environment
    if app.debug:
        file_handler.setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
    
    # Add handler to app logger
    app.logger.addHandler(file_handler)
    app.logger.info("Application started")


def get_logger(name):
    """
    Get logger instance for a module.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
