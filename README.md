# Production-Ready Flask CRUD Application with Supabase

A clean, modular Flask application for managing users with AI-powered data analysis, built for production deployment.

## Features

- **CRUD Operations**: Create, Read, Update, Delete users via REST API
- **AI Assistant**: Query database using natural language via Ollama integration
- **Modular Architecture**: Clean separation of concerns (routes, services, config)
- **Production Ready**: Logging, error handling, environment configuration
- **Database**: Supabase for reliable data persistence
- **Deployment**: Ready for Render, Heroku, or any cloud platform
- **Security**: Environment variables for secrets, CORS support

## Project Structure

```
crud/
├── app/
│   ├── __init__.py              # App factory
│   ├── config.py                # Configuration management
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py              # Main routes (/, /health)
│   │   ├── users.py             # User CRUD routes
│   │   └── ai.py                # AI query routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── supabase_service.py  # Database operations
│   │   └── ai_service.py        # AI operations
│   └── utils/
│       ├── __init__.py
│       ├── logger.py            # Logging setup
│       ├── errors.py            # Custom exceptions
│       └── validators.py        # Input validation
├── templates/
│   └── index.html               # Frontend UI
├── static/
│   ├── style.css                # Styling
│   └── script.js                # Frontend logic
├── tests/                       # Unit tests
├── run.py                       # Development entry point
├── wsgi.py                      # Production entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── Procfile                     # Render deployment config
└── runtime.txt                  # Python version for Render
```

## Installation

### 1. Clone and Setup

```bash
# Clone repository (or navigate to project directory)
cd crud

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# SUPABASE_URL and SUPABASE_KEY are required
```

### 4. Run Application

```bash
python run.py
```

Application will be available at `http://localhost:5000`

## API Endpoints

### User Management

- `GET /users` - Get all users
- `POST /users` - Create new user
- `GET /users/<id>` - Get specific user
- `PUT /users/<id>` - Update user
- `DELETE /users/<id>` - Delete user

### AI Features

- `POST /ai/query` - Query AI assistant
- `GET /ai/health` - Check AI service status

### System

- `GET /` - Frontend UI
- `GET /health` - Health check

## Request/Response Examples

### Create User

```bash
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phno": "+1 234 567 8900"
}

Response:
{
  "id": "123e4567-e89b",
  "name": "John Doe",
  "email": "john@example.com",
  "phno": "+1 234 567 8900"
}
```

### Query AI

```bash
POST /ai/query
Content-Type: application/json

{
  "question": "How many users have gmail accounts?"
}

Response:
{
  "answer": "There are 3 users with gmail accounts in the database."
}
```

## Error Handling

The application includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource doesn't exist
- **500 Internal Error**: Server-side errors
- **503 Service Unavailable**: External service unavailable (Ollama)

All errors return JSON responses with descriptive messages.

## Logging

Logs are written to `logs/app.log` with rotation:

- Development: DEBUG level
- Production: INFO level
- Maximum file size: 10MB
- Backup count: 10 files

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| FLASK_ENV | development | Environment mode |
| FLASK_HOST | 0.0.0.0 | Server host |
| FLASK_PORT | 5000 | Server port |
| SECRET_KEY | dev-key | Flask secret key |
| SUPABASE_URL | - | Supabase project URL |
| SUPABASE_KEY | - | Supabase API key |
| OLLAMA_URL | http://localhost:11434 | Ollama API URL |
| OLLAMA_MODEL | mistral | AI model to use |
| OLLAMA_TIMEOUT | 120 | Request timeout in seconds |

## Deployment on Render

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Create Render Service

1. Go to [Render Dashboard](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: your-app-name
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`

### 3. Set Environment Variables

In Render dashboard, add under "Environment":

```
FLASK_ENV=production
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
SECRET_KEY=generate-a-strong-key
```

For Ollama, you have options:
- Use a remote Ollama instance: set `OLLAMA_URL`
- Disable AI features: catch the error in frontend

### 4. Deploy

Push to main branch to auto-deploy:

```bash
git push origin main
```

## Development Workflow

### Running Tests

```bash
python -m pytest tests/
```

### Running with auto-reload

```bash
# Already enabled in development mode
python run.py
```

### Debugging

1. Set `FLASK_ENV=development`
2. Application runs in debug mode
3. Check `logs/app.log` for detailed logs

## Best Practices Implemented

✅ **Configuration Management**: Environment-based config
✅ **Modular Code**: Separated routes, services, utilities
✅ **Error Handling**: Custom exceptions, error handlers
✅ **Input Validation**: Data validation before processing
✅ **Logging**: Comprehensive logging to file
✅ **CORS Support**: Frontend/backend on different domains
✅ **Security**: Secrets in environment variables
✅ **Production Ready**: Gunicorn compatible, Render optimized
✅ **Scalable**: Service layer for easy testing/mocking
✅ **Documented**: Code comments and this README

## Troubleshooting

### Supabase Connection Error

- Verify SUPABASE_URL and SUPABASE_KEY in .env
- Check network connectivity
- Ensure table "users" exists with fields: id, name, email, phno

### Ollama Not Responding

- Start Ollama service: `ollama serve`
- Verify OLLAMA_URL is correct
- Check firewall/network settings

### Import Errors

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

## Contributing

1. Create feature branch: `git checkout -b feature/name`
2. Commit changes: `git commit -am "Add feature"`
3. Push to branch: `git push origin feature/name`
4. Submit pull request

## License

MIT License - feel free to use for personal or commercial projects.

## Support

For issues or questions:
1. Check logs in `logs/app.log`
2. Review error responses from API
3. Ensure .env is properly configured
4. Verify external services (Supabase, Ollama) are accessible
