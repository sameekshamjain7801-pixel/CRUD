"""
WSGI entry point for production deployment.
Used by Gunicorn and other production servers.
"""
import os
from app import create_app

# Create application for production
app = create_app()

if __name__ == "__main__":
    app.run()
