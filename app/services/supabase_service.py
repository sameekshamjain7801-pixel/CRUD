"""
Supabase database service.
Handles all database operations for users.
"""
from supabase import create_client, Client
from app.utils.logger import get_logger
from app.utils.errors import DatabaseError, NotFoundError
from app.config import get_config

logger = get_logger(__name__)


class SupabaseService:
    """Service for Supabase database operations"""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize Supabase client"""
        if self._initialized:
            return
        
        config = get_config()
        
        try:
            self.client: Client = create_client(
                config.SUPABASE_URL,
                config.SUPABASE_KEY
            )
            self._initialized = True
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
            raise DatabaseError(f"Failed to initialize database: {str(e)}")
    
    def get_all_users(self):
        """
        Retrieve all users from database.
        
        Returns:
            List of user dictionaries
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            response = self.client.table("users").select("*").execute()
            logger.info(f"Retrieved {len(response.data)} users")
            return response.data
        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            raise DatabaseError(f"Failed to fetch users: {str(e)}")
    
    def get_user_by_id(self, user_id):
        """
        Retrieve a single user by ID.
        
        Args:
            user_id: User ID to retrieve
            
        Returns:
            User dictionary
            
        Raises:
            NotFoundError: If user doesn't exist
            DatabaseError: If database operation fails
        """
        try:
            response = self.client.table("users").select("*").eq("id", user_id).execute()
            
            if not response.data:
                raise NotFoundError("User", user_id)
            
            logger.info(f"Retrieved user with ID: {user_id}")
            return response.data[0]
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to fetch user: {str(e)}")
    
    def create_user(self, user_data):
        """
        Create a new user in database.
        
        Args:
            user_data: Dictionary containing user information
                      (name, email, phno)
            
        Returns:
            Created user data
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            response = self.client.table("users").insert(user_data).execute()
            logger.info(f"Created user: {user_data.get('email')}")
            return response.data[0] if response.data else user_data
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    def update_user(self, user_id, user_data):
        """
        Update an existing user.
        
        Args:
            user_id: User ID to update
            user_data: Dictionary with fields to update
            
        Returns:
            Updated user data
            
        Raises:
            NotFoundError: If user doesn't exist
            DatabaseError: If database operation fails
        """
        try:
            # Verify user exists
            self.get_user_by_id(user_id)
            
            response = self.client.table("users").update(user_data).eq("id", user_id).execute()
            logger.info(f"Updated user with ID: {user_id}")
            return response.data[0] if response.data else user_data
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to update user: {str(e)}")
    
    def delete_user(self, user_id):
        """
        Delete a user from database.
        
        Args:
            user_id: User ID to delete
            
        Raises:
            NotFoundError: If user doesn't exist
            DatabaseError: If database operation fails
        """
        try:
            # Verify user exists before deletion
            self.get_user_by_id(user_id)
            
            self.client.table("users").delete().eq("id", user_id).execute()
            logger.info(f"Deleted user with ID: {user_id}")
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete user: {str(e)}")
