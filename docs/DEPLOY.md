# Deployment Guide for TYC Islamic Finance Advisor

This guide will help you deploy the web application to Render (free tier) for wider sharing.

## Option 1: Deploy to Render (Recommended - Free & Easy)

### Step 1: Create a GitHub Repository

1. Go to https://github.com and create a new repository
2. Initialize git in your project folder:
   ```bash
   cd /Users/bilalbai/Desktop/tyc-gpt
   git init
   git add .
   git commit -m "Initial commit"
   ```
3. Push to GitHub:
   ```bash
   git remote add origin YOUR_GITHUB_REPO_URL
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. Go to https://render.com and sign up/login (free account)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: tyc-islamic-finance-advisor (or any name you like)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or choose a paid plan)
5. Go to "Environment" tab and add:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key (from your .env file)
6. Click "Create Web Service"
7. Wait for deployment (usually 2-3 minutes)
8. Your app will be live at: `https://your-app-name.onrender.com`

### Step 3: Share Your Link

Once deployed, you'll get a URL like:
- `https://tyc-islamic-finance-advisor.onrender.com`

Share this link with anyone, anywhere in the world!

---

## Option 2: Deploy to Railway (Alternative - Free Tier)

1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your repository
4. Add environment variable:
   - `OPENAI_API_KEY` = your API key
5. Railway will auto-detect Python and deploy
6. Get your public URL from the settings

---

## Option 3: Deploy to Fly.io (Alternative)

1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. Run: `fly launch`
3. Follow the prompts
4. Set secret: `fly secrets set OPENAI_API_KEY=your_key_here`
5. Deploy: `fly deploy`

---

## Option 4: Quick Test with ngrok (Temporary Sharing)

If you just want to quickly share for testing:

1. Install ngrok: https://ngrok.com/download
2. Start your Flask app: `python app.py`
3. In another terminal: `ngrok http 5000`
4. Share the ngrok URL (e.g., `https://abc123.ngrok.io`)
5. Note: Free ngrok URLs expire after a few hours

---

## Important Notes

- **Never commit your .env file** - it's already in .gitignore
- **Always set OPENAI_API_KEY as an environment variable** in your deployment platform
- **Free tiers may have cold starts** - first request after inactivity may be slow
- **Monitor your OpenAI usage** - API calls cost money based on usage

---

## Troubleshooting

### App won't start
- Check that `gunicorn` is in requirements.txt
- Verify the start command is correct: `gunicorn app:app`
- Check logs in your deployment platform's dashboard

### 500 Errors
- Verify OPENAI_API_KEY is set correctly in environment variables
- Check that your OpenAI account has credits/quota

### Slow responses
- Free tiers may have resource limits
- Consider upgrading to a paid plan for better performance

---

## Cost Considerations

- **Render Free Tier**: Free, but apps sleep after 15 minutes of inactivity
- **OpenAI API**: Pay per use (check pricing at openai.com/pricing)
- **Recommended**: Start with free tier, upgrade if you get traffic

