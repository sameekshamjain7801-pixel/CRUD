# ⚡ Quick Start Guide

Get your production-ready Flask app running in **5 minutes**.

## 1️⃣ Setup (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2️⃣ Configure (1 minute)

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your Supabase credentials:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-api-key
```

## 3️⃣ Run (30 seconds)

```bash
python run.py
```

Open browser: http://localhost:5000 ✅

## 4️⃣ API Tests

```bash
# Create user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","phno":"+1234567890"}'

# Get all users
curl http://localhost:5000/users

# Query AI (with Ollama running)
curl -X POST http://localhost:5000/ai/query \
  -H "Content-Type: application/json" \
  -d '{"question":"How many users?"}'
```

## 5️⃣ Deployment

Push to GitHub and deploy on Render:

1. Create Web Service on Render
2. Set environment variables
3. Deploy with: `gunicorn wsgi:app`

See `DEPLOYMENT.md` for details.

---

## 📁 Project Structure

```
app/                    # Main application
├── routes/             # API endpoints
├── services/           # Business logic
├── utils/              # Helpers & errors
├── config.py           # Configuration
└── __init__.py         # App factory

run.py                  # Development server
wsgi.py                 # Production server
requirements.txt        # Dependencies
.env.example            # Config template
```

---

## 📖 Full Documentation

- **README.md** - Complete project documentation
- **MIGRATION.md** - What changed from old structure
- **DEPLOYMENT.md** - How to deploy on Render
- **REFACTORING_SUMMARY.md** - All improvements made

---

## ✅ Features

- ✅ User CRUD API (create, read, update, delete)
- ✅ AI query with Ollama
- ✅ Error handling & validation
- ✅ Logging to file
- ✅ Environment configuration
- ✅ CORS enabled
- ✅ Production deployment ready
- ✅ Health check endpoints

---

## 🆘 Troubleshooting

### Module not found error
```bash
pip install -r requirements.txt
```

### Supabase connection error
Check your `.env` file has correct SUPABASE_URL and SUPABASE_KEY

### Port already in use
Edit `.env` and change FLASK_PORT to 5001

### Ollama not responding
Start Ollama: `ollama serve`

---

## 🚀 Next Steps

1. Run locally to verify setup
2. Test API endpoints
3. Push to GitHub
4. Deploy on Render (DEPLOYMENT.md)
5. Monitor with `/health` endpoint

**You're ready to deploy!** 🎉
