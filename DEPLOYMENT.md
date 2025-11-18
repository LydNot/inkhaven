# 🚀 Deployment Guide

## Quick Deploy to Render.com (Recommended)

### Step 1: Push to GitHub

```bash
cd /Users/mox/inkhaven-database
git init
git add .
git commit -m "Initial commit - Inkhaven Post Explorer"
```

Create a new repository on GitHub, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/inkhaven-explorer.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up (free!)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `inkhaven-explorer`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`
   - **Instance Type**: Free

5. **Add Environment Variable**:
   - Key: `ANTHROPIC_API_KEY`
   - Value: `your-anthropic-api-key-here` (DO NOT commit your actual key!)

6. Click **"Create Web Service"**

### Step 3: Your Site is Live! 🎉

Render will give you a URL like: `https://inkhaven-explorer.onrender.com`

**Note**: The free tier spins down after inactivity, so first load may take 30 seconds.

---

## 🌐 Custom Domain (Optional)

### If you want your own domain:

1. **Buy a domain** from:
   - [Namecheap](https://namecheap.com) (~$10/year)
   - [Google Domains](https://domains.google) (~$12/year)
   - [Cloudflare](https://cloudflare.com) (~$10/year)

2. **Connect to Render**:
   - In Render dashboard, go to your service → Settings → Custom Domain
   - Add your domain (e.g., `inkhaven-explorer.com`)
   - Follow the DNS instructions to update your domain's CNAME records

---

## Alternative: Railway.app

Similar to Render, also has a free tier:

1. Go to [railway.app](https://railway.app)
2. **"New Project"** → **"Deploy from GitHub"**
3. Select your repo
4. Add environment variable: `ANTHROPIC_API_KEY`
5. Railway auto-detects Python and deploys!

---

## Alternative: Vercel (Frontend-focused)

Best for static sites, requires more work for the backend:

1. Deploy frontend to Vercel
2. Deploy backend separately (Render/Railway)
3. Update API URLs in index.html

---

## 🔄 Continuous Deployment

Once set up, just push to GitHub:

```bash
git add .
git commit -m "Update tags"
git push
```

Render/Railway will automatically redeploy! 🚀

---

## ⚠️ Important Notes

1. **Data Persistence**: The free tiers use ephemeral storage, meaning:
   - `tagged_posts.json` will reset on redeploy
   - `community_tags.json` will reset on redeploy
   - Consider upgrading to a paid tier or using a database for permanent storage

2. **Background Tagging**: The `tagger.py` script won't run automatically on free tiers
   - You'll need to run it manually on your computer
   - Or set up a scheduled job (Render Cron Jobs - paid tier)

3. **API Key Security**: Environment variables keep your API key safe!

---

## 💾 For Persistent Storage (Optional Upgrade)

Consider using:
- PostgreSQL database (free on Render/Railway)
- MongoDB Atlas (free tier available)
- Supabase (free tier available)

This requires modifying `server.py` to use a database instead of JSON files.

