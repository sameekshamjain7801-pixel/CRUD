# Migration & Setup Guide

## Quick Start

### 1. Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your Supabase credentials
# Required:
#   SUPABASE_URL=https://your-project.supabase.co
#   SUPABASE_KEY=your-api-key
```

### 4. Run Application

```bash
# Development with auto-reload
python run.py

# Production with Gunicorn
gunicorn wsgi:app
```

Application will be at: http://localhost:5000

---

## What Changed: Old vs New

### Monolithic vs Modular

**Old Structure:**
```
crud/
├── app.py (everything in one file)
├── templates/index.html
├── static/script.js
├── static/style.css
└── requirements.txt
```

**New Structure:**
```
crud/
├── app/                    # Application package
│   ├── __init__.py        # App factory
│   ├── config.py          # Configuration
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   └── utils/             # Helpers & errors
├── templates/             # Frontend
├── static/                # Assets
├── tests/                 # Unit tests
├── run.py                 # Dev entry point
├── wsgi.py                # Prod entry point
├── README.md              # Documentation
├── DEPLOYMENT.md          # Deployment guide
├── requirements.txt       # Dependencies
├── .env.example           # Config template
├── .gitignore             # Git rules
├── Procfile               # Render config
└── runtime.txt            # Python version
```

### Configuration Management

**Old:**
```python
load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
ollama_url = "http://localhost:11434"  # Hardcoded!
```

**New:**
```python
# app/config.py - Centralized, validated
class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    # Environment-specific configs possible
```

### API Routes

**Old (Monolithic):**
```python
@app.route("/users", methods=["GET"])
def get_users():
    # Everything in one file
```

**New (Blueprints):**
```
routes/
├── main.py   # GET / (index), GET /health
├── users.py  # All user CRUD operations
└── ai.py     # AI queries
```

### Business Logic

**Old:**
```python
@app.route("/users", methods=["GET"])
def get_users():
    try:
        response = supabase.table("users").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

**New (Service Layer):**
```python
# In routes/users.py
from app.services import SupabaseService

@users_bp.route("", methods=["GET"])
def get_all_users():
    try:
        users = supabase_service.get_all_users()
        return jsonify(users), 200
    except AppError as e:
        return jsonify(e.to_dict()), e.status_code

# In services/supabase_service.py
def get_all_users(self):
    try:
        response = self.client.table("users").select("*").execute()
        logger.info(f"Retrieved {len(response.data)} users")
        return response.data
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise DatabaseError(f"Failed to fetch users: {str(e)}")
```

### Error Handling

**Old:**
```python
except Exception as e:
    return jsonify({"error": str(e)}), 500  # All errors same
```

**New:**
```python
# Custom exception hierarchy
class AppError(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code

class ValidationError(AppError):
    def __init__(self, message):
        super().__init__(message, status_code=400)

class NotFoundError(AppError):
    def __init__(self, resource_name, resource_id=None):
        # Specific error messages

# Usage in routes
except ValidationError as e:
    return jsonify(e.to_dict()), e.status_code  # 400
except NotFoundError as e:
    return jsonify(e.to_dict()), e.status_code  # 404
```

### Logging

**Old:**
```python
# No logging configured
print(f"Ollama error: {ollama_response.status_code}")
```

**New:**
```python
# Centralized logging
logger = get_logger(__name__)
logger.info("Successfully processed AI query")
logger.error(f"Error fetching users: {str(e)}")
# Logs go to logs/app.log with rotation
```

### Input Validation

**Old:**
```python
# No validation
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json  # No checks!
    response = supabase.table("users").insert(data).execute()
```

**New:**
```python
# Validators before processing
def validate_user_data(data):
    required_fields = ["name", "email", "phno"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing: {', '.join(missing_fields)}")
    validate_email(data["email"])

# In routes
try:
    validate_user_data(data)
    user = supabase_service.create_user(data)
```

### Environment Variables

**Old:**
```bash
# Required: .env in root with correct values
SUPABASE_URL=...
SUPABASE_KEY=...
# Hardcoded values for others
```

**New:**
```bash
# .env.example provided for reference
# Only two REQUIRED:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-api-key

# Optional (defaults provided):
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=dev-key-change-in-production
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_TIMEOUT=120
```

### Dependencies

**Old:**
```
flask
supabase
python-dotenv
requests
```

**New:**
```
flask==3.0.0                # Web framework
supabase==2.4.2             # Database
python-dotenv==1.0.0        # Environment config
requests==2.31.0            # HTTP client
gunicorn==21.2.0            # Production server
flask-cors==4.0.0           # CORS support
```

Pinned versions for reproducible deployments!

### Deployment

**Old:**
- No deployment configuration
- Not production-ready
- Hardcoded values problematic

**New:**
- `Procfile` - For Render deployment
- `runtime.txt` - Python version specification
- `wsgi.py` - Production entry point
- `gunicorn` - Production-grade server
- `DEPLOYMENT.md` - Complete deployment guide

---

## API Changes

### Endpoint Changes

| Operation | Old Path | New Path | Status |
|-----------|----------|----------|--------|
| Get all users | GET /users | GET /users | ✅ Same |
| Create user | POST /users | POST /users | ✅ Same |
| Get single | GET /users/<id> | GET /users/<id> | ✅ Same |
| Update user | PUT /users/<id> | PUT /users/<id> | ✅ Same |
| Delete user | DELETE /users/<id> | DELETE /users/<id> | ✅ Same |
| Query AI | POST /ai | POST /ai/query | ⚠️ Changed |
| Health check | N/A | GET /health | ✅ New |
| AI health | N/A | GET /ai/health | ✅ New |

### Response Changes

**Error responses now use consistent format:**

```json
{
  "error": "User with ID 'invalid' not found"
}
```

With appropriate HTTP status codes:
- 400: Bad Request (validation errors)
- 404: Not Found
- 500: Server Error
- 503: Service Unavailable

---

## Migration Checklist

- [ ] Create virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Add Supabase credentials to `.env`
- [ ] Run application: `python run.py`
- [ ] Test endpoints (all should work)
- [ ] Push to GitHub
- [ ] Deploy on Render (see DEPLOYMENT.md)
- [ ] Delete old `app.py` (it's replaced by modular structure)
- [ ] Test production deployment
- [ ] Configure custom domain (optional)

---

## Troubleshooting Migration

### Import Errors

```
ModuleNotFoundError: No module named 'app'
```

**Solution:** Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

### SUPABASE_URL not found

```
ValueError: Missing required environment variables: SUPABASE_URL, SUPABASE_KEY
```

**Solution:** Configure `.env` file:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Port Already in Use

```
OSError: [Errno 10048] Only one usage of each socket address
```

**Solution:** Change port in `.env`:
```
FLASK_PORT=5001
```

Or kill process using port 5000.

### AI Service Errors

```
ExternalServiceError: Ollama service is not running
```

**Solution:** Start Ollama service:
```bash
ollama serve
```

Or disable AI features in deployment.

---

## Key Improvements

1. **✅ Modular Architecture** - Easy to maintain and test
2. **✅ Configuration Management** - Environment-based, no hardcoding
3. **✅ Error Handling** - Specific exceptions, proper HTTP status codes
4. **✅ Logging** - Comprehensive logging to file
5. **✅ Input Validation** - Data validation before processing
6. **✅ Production Ready** - Gunicorn, Render deployment
7. **✅ Security** - Secrets in .env, CORS support
8. **✅ Documentation** - README, deployment guide, code comments
9. **✅ Scalability** - Service layer for easy mocking/testing
10. **✅ Testing** - Basic test structure provided

---

## Next Steps

1. **Run locally** to verify everything works
2. **Deploy to Render** (see DEPLOYMENT.md)
3. **Monitor logs** in production
4. **Add tests** in `tests/` folder
5. **Optimize** based on monitoring data

Enjoy your production-ready Flask application! 🚀
