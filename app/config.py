"""
Configuration management for Flask application.
Supports multiple environments (development, testing, production).
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = False
    TESTING = False
    
    # Supabase configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # AI configuration
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
    
    # Application settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    @staticmethod
    def validate_config():
        """Validate that all required configuration is present"""
        required_keys = ["SUPABASE_URL", "SUPABASE_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_keys)}. "
                "Please check your .env file."
            )


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = False
    TESTING = True


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False


# Configuration dictionary
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config():
    """Get configuration based on FLASK_ENV environment variable"""
    env = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
