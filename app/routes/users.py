"""
User management routes.
Handles CRUD operations for users.
"""
from flask import Blueprint, request, jsonify
from app.services import SupabaseService
from app.utils import ValidationError, get_logger, validate_user_data
from app.utils.errors import AppError

logger = get_logger(__name__)
users_bp = Blueprint("users", __name__, url_prefix="/users")
supabase_service = SupabaseService()


@users_bp.route("", methods=["GET"])
def get_all_users():
    """
    Retrieve all users.
    
    Returns:
        JSON list of users
    """
    try:
        users = supabase_service.get_all_users()
        return jsonify(users), 200
    except AppError as e:
        logger.warning(f"Validation error: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_all_users: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.route("", methods=["POST"])
def create_user():
    """
    Create a new user.
    
    Request JSON:
        - name: str (required)
        - email: str (required)
        - phno: str (required)
    
    Returns:
        JSON object with created user
    """
    try:
        data = request.get_json()
        validate_user_data(data)
        
        user = supabase_service.create_user(data)
        logger.info(f"User created: {data.get('email')}")
        return jsonify(user), 201
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except AppError as e:
        logger.error(f"Application error: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in create_user: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Retrieve a specific user by ID.
    
    Args:
        user_id: User ID (from URL parameter)
    
    Returns:
        JSON object with user data
    """
    try:
        user = supabase_service.get_user_by_id(user_id)
        return jsonify(user), 200
        
    except AppError as e:
        logger.warning(f"Error retrieving user {user_id}: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_user: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update an existing user.
    
    Args:
        user_id: User ID (from URL parameter)
    
    Request JSON:
        - name: str (optional)
        - email: str (optional)
        - phno: str (optional)
    
    Returns:
        JSON object with updated user
    """
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("Request body cannot be empty")
        
        user = supabase_service.update_user(user_id, data)
        logger.info(f"User updated: {user_id}")
        return jsonify(user), 200
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except AppError as e:
        logger.error(f"Application error: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in update_user: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user by ID.
    
    Args:
        user_id: User ID (from URL parameter)
    
    Returns:
        JSON with success message
    """
    try:
        supabase_service.delete_user(user_id)
        logger.info(f"User deleted: {user_id}")
        return jsonify({"message": "User deleted successfully"}), 200
        
    except AppError as e:
        logger.warning(f"Error deleting user {user_id}: {e.message}")
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in delete_user: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
