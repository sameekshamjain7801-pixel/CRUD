"""
Unit tests for the application.
"""
import pytest
from app import create_app
from app.config import TestingConfig


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app(TestingConfig)
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestMainRoutes:
    """Tests for main routes"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'


class TestUserRoutes:
    """Tests for user CRUD routes"""
    
    def test_get_users_empty(self, client):
        """Test getting users when none exist"""
        response = client.get('/users')
        assert response.status_code == 200
        # Note: In real tests, mock Supabase


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        assert 'error' in response.json


if __name__ == '__main__':
    pytest.main([__file__])
