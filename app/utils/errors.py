"""
Custom exception classes for the application.
"""


class AppError(Exception):
    """Base exception for all application errors"""
    
    def __init__(self, message, status_code=500):
        super().__init__()
        self.message = message
        self.status_code = status_code
    
    def to_dict(self):
        """Convert exception to dictionary for JSON response"""
        return {"error": self.message}


class ValidationError(AppError):
    """Raised when request validation fails"""
    
    def __init__(self, message):
        super().__init__(message, status_code=400)


class NotFoundError(AppError):
    """Raised when resource is not found"""
    
    def __init__(self, resource_name, resource_id=None):
        if resource_id:
            message = f"{resource_name} with ID '{resource_id}' not found"
        else:
            message = f"{resource_name} not found"
        super().__init__(message, status_code=404)


class DatabaseError(AppError):
    """Raised when database operation fails"""
    
    def __init__(self, message):
        super().__init__(f"Database error: {message}", status_code=500)


class ExternalServiceError(AppError):
    """Raised when external service (Ollama, Supabase) fails"""
    
    def __init__(self, service_name, message):
        super().__init__(
            f"{service_name} service error: {message}",
            status_code=503
        )


class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass
