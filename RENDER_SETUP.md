# Render Deployment - Complete Setup Guide

## Your GitHub Repository
🔗 https://github.com/sameekshamjain7801-pixel/CRUD

---

## Step 1: Create Render Account (if needed)

1. Go to https://render.com
2. Sign up with GitHub (or email)
3. Click "New +" → "Web Service"

---

## Step 2: Connect GitHub Repository

1. In Render Dashboard, click **"New +" → "Web Service"**
2. Click **"Connect a repository"**
3. Select **"sameekshamjain7801-pixel/CRUD"** from the list
4. If not showing, click "Configure account" to authorize GitHub

---

## Step 3: Configure Web Service

Fill in the following settings:

| Field | Value |
|-------|-------|
| **Name** | `crud-app` (or any name) |
| **Environment** | `Python 3` |
| **Region** | `Oregon` (closest to you) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn wsgi:app` |

---

## Step 4: Add Environment Variables

Click **"Add Environment Variable"** and add these:

```
FLASK_ENV=production
SECRET_KEY=<generate-random-key-below>
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-api-key
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

### Generate SECRET_KEY

Use this command in terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as `SECRET_KEY` value.

### Get Supabase Credentials

1. Go to https://supabase.com
2. Open your project
3. Click **Settings** → **API**
4. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **Anon Key** → `SUPABASE_KEY`

---

## Step 5: Deploy

Click **"Create Web Service"** button.

Render will:
1. Clone your repository
2. Install dependencies
3. Start the application
4. Provide a public URL

**This takes 2-3 minutes** ⏳

---

## Step 6: Verify Deployment

Once deployed, you'll see a URL like: `https://crud-app.onrender.com`

### Test the endpoints:

```bash
# Health check
curl https://crud-app.onrender.com/health

# Get users
curl https://crud-app.onrender.com/users

# Create user
curl -X POST https://crud-app.onrender.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","phno":"+1234567890"}'
```

---

## Step 7: Monitor Your Application

### View Logs

1. Go to Render Dashboard → Your service
2. Click **"Logs"** tab
3. Watch real-time logs

### Check Application Status

- **Green dot** = Running ✅
- **Red dot** = Failed ❌
- Check logs if red

### Common Issues in Logs

```
ModuleNotFoundError: No module named 'app'
→ Check Python import paths in code

missing required environment variables
→ Add SUPABASE_URL and SUPABASE_KEY in environment

connection refused
→ Supabase URL/key incorrect
```

---

## Step 8: Set Custom Domain (Optional)

1. Go to Render Dashboard → Your service
2. Click **"Settings"** tab
3. Scroll to "Custom Domain"
4. Enter your domain (e.g., `myapp.com`)
5. Update DNS records as shown
6. SSL certificate auto-generated! 🔒

---

## Important Notes

### Free Tier Limitations

- **Spins down** after 15 min of inactivity (takes 30 sec to restart)
- **Limited resources** (0.5 CPU, 512MB RAM)
- Good for development/testing

### Upgrade to Paid

For production:
1. Click **"Plan"** in service settings
2. Select **"Standard"** ($7/month)
3. Features: No spin-down, better performance

---

## Troubleshooting

### Build Fails

**Error:** "pip install failed"

**Solution:**
1. Check `requirements.txt` syntax
2. Verify Python packages are compatible
3. Click "Clear build cache" in Render

### Service Won't Start

**Error:** "Application failed to start"

**Solution:**
1. Check logs for error messages
2. Verify all environment variables are set
3. Ensure `wsgi.py` is in root directory

### Database Connection Error

**Error:** "SUPABASE_URL not found"

**Solution:**
1. Add `SUPABASE_URL` and `SUPABASE_KEY` environment variables
2. Verify values are correct (no extra spaces)
3. Redeploy

### AI Service Unavailable

**Error:** "Ollama is not running"

**Solution:**
- This is expected on Render (no local Ollama)
- Either:
  - Use a remote Ollama instance (set `OLLAMA_URL`)
  - Or remove AI features for deployment

---

## Auto-Deployment

Every time you push to GitHub, Render automatically deploys:

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Render auto-deploys in 1-2 minutes
# Check "Deployments" tab to watch progress
```

---

## View Deployment History

1. Render Dashboard → Your service
2. Click **"Deployments"** tab
3. See all deployments and rollback if needed

---

## Your Application URLs

- **Main App:** `https://crud-app.onrender.com`
- **API Base:** `https://crud-app.onrender.com/users`
- **Health Check:** `https://crud-app.onrender.com/health`

Replace `crud-app` with your actual service name.

---

## Next Steps

1. ✅ Add environment variables
2. ✅ Click "Create Web Service"
3. ✅ Wait for deployment
4. ✅ Test endpoints
5. ✅ Monitor logs
6. ✅ Update GitHub to auto-deploy
7. ✅ Add custom domain (optional)

---

## Support Resources

- **Render Docs:** https://render.com/docs
- **Application README:** See `README.md` in repo
- **Deployment Guide:** See `DEPLOYMENT.md` in repo
- **Error Logs:** Check Render dashboard logs

---

## Quick Checklist ✅

- [ ] GitHub repository created and pushed
- [ ] Render account created
- [ ] Web Service created
- [ ] Environment variables added
- [ ] Deployment started
- [ ] Application running (green dot)
- [ ] Health check endpoint working
- [ ] Database connection verified
- [ ] Custom domain added (optional)
- [ ] Monitoring set up

You're all set! Your app is live! 🚀
