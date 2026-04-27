# RENDER DEPLOYMENT - QUICK STEPS

## 9 Steps to Deploy Your App

---

### **STEP 1: Open Render**
- Go to https://render.com
- Log in with your account

---

### **STEP 2: Create New Service**
- Click **"New +"** button (top right)
- Click **"Web Service"**

---

### **STEP 3: Connect GitHub**
- Click **"Connect a repository"**
- Find and select **"sameekshamjain7801-pixel/CRUD"**
- Click **"Connect"**

---

### **STEP 4: Set Service Name**
- Name: **crud-app**
- Region: **Oregon**
- Branch: **main**

---

### **STEP 5: Set Build & Start Commands**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn wsgi:app`

---

### **STEP 6: Add Environment Variables**

Click **"Add Environment Variable"** and add:

#### Variable 1:
```
Key: FLASK_ENV
Value: production
```

#### Variable 2:
```
Key: SECRET_KEY
Value: [Run this in terminal and copy output]:
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Variable 3:
```
Key: SUPABASE_URL
Value: https://your-project.supabase.co
[Get from: supabase.com → Your Project → Settings → API]
```

#### Variable 4:
```
Key: SUPABASE_KEY
Value: your-anon-key-here
[Get from: supabase.com → Your Project → Settings → API → Anon Key]
```

---

### **STEP 7: Review Settings**

Check:
- ✅ Service name: crud-app
- ✅ Environment: Python 3
- ✅ Build Command correct
- ✅ Start Command correct
- ✅ 4 Environment variables added

---

### **STEP 8: Deploy**
- Click **"Create Web Service"** button
- **Wait 2-3 minutes**

---

### **STEP 9: Check Status**
- Look for **green dot** ✅ next to service name
- Your URL will appear (e.g., https://crud-app.onrender.com)
- Click the URL to open your live app

---

## VERIFY IT WORKS

Open your browser:
```
https://crud-app.onrender.com/health
```

You should see:
```
{"status": "healthy"}
```

---

## DONE! 🎉

Your app is now **LIVE** and hosted on Render!

### Automatic Updates
Push code to GitHub:
```
git push origin main
```
→ Render automatically deploys in 1-2 minutes!

---

## TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Red X status | Check "Logs" tab for errors |
| "Environment variable not found" | Add missing env var in Step 6 |
| "Connection refused" | Check SUPABASE_URL and SUPABASE_KEY |
| 503 error | Wait - service might still be starting |

---

## YOUR LIVE APP

- **Main URL:** https://crud-app.onrender.com
- **API Users:** https://crud-app.onrender.com/users
- **Health:** https://crud-app.onrender.com/health

(Replace "crud-app" with your actual service name)

---

**Questions? Check RENDER_SETUP.md in your GitHub repo for details!**
