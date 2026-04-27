"""
AI routes.
Handles AI-powered queries on database.
"""
from flask import Blueprint, request, jsonify
from app.services import SupabaseService, AIService
from app.utils import ValidationError, get_logger, validate_question
from app.utils.errors import AppError

logger = get_logger(__name__)
ai_bp = Blueprint("ai", __name__, url_prefix="/ai")
supabase_service = SupabaseService()
ai_service = AIService()


@ai_bp.route("/query", methods=["POST"])
def query_ai():
    """
    Query AI with a question based on database context.
    
    Request JSON:
        - question: str (required) - The question to ask AI
    
    Returns:
        JSON object with AI response
    """
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("Request body cannot be empty")
        
        question = data.get("question", "").strip()
        validate_question(question)
        
        # Fetch context data from database
        users_data = supabase_service.get_all_users()
        
        if not users_data:
            logger.info("No user data available for AI analysis")
            return jsonify({"answer": "No data available to analyze"}), 200
        
        # Query AI with context
        answer = ai_service.query_ai(question, users_data)
        logger.info(f"AI query processed successfully")
        return jsonify({"answer": answer}), 200
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except AppError as e:
        logger.error(f"Application error: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in query_ai: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@ai_bp.route("/health", methods=["GET"])
def ai_health():
    """
    Check if AI service is available.
    
    Returns:
        JSON with status
    """
    try:
        # Try to verify Ollama is accessible
        import requests
        from app.config import get_config
        
        config = get_config()
        response = requests.get(
            f"{config.OLLAMA_URL}/api/tags",
            timeout=5
        )
        
        if response.status_code == 200:
            return jsonify({"status": "healthy", "service": "Ollama"}), 200
        else:
            return jsonify({"status": "unhealthy"}), 503
            
    except Exception as e:
        logger.warning(f"AI service health check failed: {str(e)}")
        return jsonify({"status": "unavailable"}), 503
