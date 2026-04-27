# Deployment Guide for Render

## Prerequisites

- GitHub repository with the code
- Render account (https://render.com)
- Supabase project with credentials

## Step-by-Step Deployment

### 1. Prepare Your Repository

```bash
# Make sure all files are committed
git add .
git commit -m "Production-ready refactored Flask app"
git push
```

### 2. Create Render Web Service

1. Log in to Render Dashboard
2. Click "New" → "Web Service"
3. Select your GitHub repository
4. Configure service:

```
Name: your-app-name
Environment: Python 3
Region: Oregon (or your preferred)
Build Command: pip install -r requirements.txt
Start Command: gunicorn wsgi:app
```

### 3. Set Environment Variables

Click "Add Environment Variable" and add:

```
FLASK_ENV=production
SECRET_KEY=<generate-a-strong-random-key>
SUPABASE_URL=<your-supabase-url>
SUPABASE_KEY=<your-supabase-anon-key>
OLLAMA_URL=<your-remote-ollama-url or skip if not needed>
OLLAMA_MODEL=mistral
```

### 4. Create Build Script (Optional)

If you need to run migrations or setup tasks, create `build.sh`:

```bash
#!/bin/bash
pip install -r requirements.txt
# Add any initialization commands here
```

Then update Procfile:
```
web: gunicorn wsgi:app
```

### 5. Deploy

Click "Create Web Service" and Render will:
1. Clone your repository
2. Install dependencies
3. Start the application
4. Provide a URL (e.g., https://your-app.onrender.com)

## Monitoring Deployment

1. Check "Logs" tab for real-time output
2. Verify application is running (should see logs)
3. Check `/health` endpoint:
   ```bash
   curl https://your-app.onrender.com/health
   ```

## Troubleshooting Deployment

### Build Fails

- Check logs for Python version compatibility
- Verify all dependencies in requirements.txt
- Ensure no import errors

### Application Won't Start

- Check environment variables are set
- Verify SUPABASE_URL and SUPABASE_KEY
- Check application logs

### Service Unavailable

- Check if free tier has exceeded resource limits
- Upgrade to paid plan if needed
- Check Render dashboard for service status

## Accessing Your Application

- **Web URL**: https://your-app.onrender.com
- **API**: https://your-app.onrender.com/users
- **Health Check**: https://your-app.onrender.com/health

## Auto-Deployment

Render automatically deploys when you push to main branch:

```bash
git push origin main
```

Check the "Deployments" tab to see deployment history.

## Environment-Specific Configuration

For different environments, use different secrets:

### Development
- FLASK_ENV=development
- SECRET_KEY=dev-key (less important)

### Production
- FLASK_ENV=production
- SECRET_KEY=generate-strong-key
- Use environment-specific Supabase projects

## Performance Optimization

1. **Use paid tier** for better performance on Render
2. **Set appropriate timeouts** for OLLAMA_TIMEOUT
3. **Monitor logs** for slow queries
4. **Scale horizontally** if needed

## Security Best Practices

1. ✅ Never commit .env file
2. ✅ Rotate SECRET_KEY regularly
3. ✅ Use separate Supabase keys for production
4. ✅ Enable CORS only for trusted domains
5. ✅ Monitor logs for suspicious activity
6. ✅ Update dependencies regularly

## Rollback

If deployment has issues:

1. Go to "Deployments" tab
2. Find previous working deployment
3. Click "Deploy" to rollback
4. Or disable service and redeploy

## SSL/HTTPS

Render automatically provides HTTPS for all services. Your site is secure by default!

## Custom Domain

1. Go to "Settings" tab
2. Add custom domain
3. Update DNS records as shown
4. SSL certificate is auto-generated

## Database Backup

Your Supabase database is managed separately:

1. Log in to Supabase
2. Go to "Backups"
3. Configure backup schedule
4. Download backups as needed

## Support

- Render Docs: https://render.com/docs
- Application Logs: Check Render dashboard
- Errors: Check logs directory in application
