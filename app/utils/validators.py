"""
Input validation utilities.
"""
import re
from app.utils.errors import ValidationError


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Raises:
        ValidationError: If email format is invalid
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")


def validate_user_data(data):
    """
    Validate user creation/update data.
    
    Args:
        data: Dictionary containing user data
        
    Raises:
        ValidationError: If data is invalid
    """
    if not data:
        raise ValidationError("Request body cannot be empty")
    
    # Check required fields for create operation
    required_fields = ["name", "email", "phno"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Validate email
    validate_email(data["email"])
    
    # Validate name length
    if not 1 <= len(str(data["name"]).strip()) <= 255:
        raise ValidationError("Name must be between 1 and 255 characters")
    
    # Validate phone number (basic check)
    phone = str(data["phno"]).strip()
    if not 5 <= len(phone) <= 20:
        raise ValidationError("Phone number must be between 5 and 20 characters")


def validate_question(question):
    """
    Validate AI question input.
    
    Args:
        question: Question text
        
    Raises:
        ValidationError: If question is invalid
    """
    if not question or not str(question).strip():
        raise ValidationError("Question cannot be empty")
    
    question_text = str(question).strip()
    if len(question_text) > 1000:
        raise ValidationError("Question must be less than 1000 characters")
