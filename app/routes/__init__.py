"""Routes package"""
from app.routes.main import main_bp
from app.routes.users import users_bp
from app.routes.ai import ai_bp

__all__ = ["main_bp", "users_bp", "ai_bp"]
