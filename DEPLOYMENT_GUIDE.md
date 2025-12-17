# Deployment Guide - Render

## Problem: Secrets in Git

Your `service_account.json` contains sensitive credentials that should **never** be committed to Git. GitHub's push protection correctly blocked this.

## Solution: Store Secrets in Render

### Step 1: Remove Secret from Git History

```bash
# Remove the file from git tracking
git rm --cached utils/service_account.json

# Commit the removal
git commit -m "Remove service_account.json - use environment variables"

# Force push (already blocked, but this shows the fix)
git push
```

### Step 2: Prepare Credentials for Render

#### Option A: String Format (Easiest)
1. Get your `service_account.json` content
2. Convert to single-line JSON:
   ```bash
   cat utils/service_account.json | python -c "import sys, json; print(json.dumps(json.load(sys.stdin)))"
   ```
3. Copy the output

#### Option B: Keep File Format
- Upload `service_account.json` separately to Render

### Step 3: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Create new **Web Service**
3. Connect your GitHub repository
4. Fill in settings:
   - **Name**: job-alerts
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 4: Set Environment Variables in Render

1. In Render dashboard, go to **Environment**
2. Add these variables:

```
SENDGRID_API_KEY=your_sendgrid_key
JWT_SECRET=your_jwt_secret_key
BASE_URL=https://your-app.onrender.com
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"..."}
```

**For FIREBASE_SERVICE_ACCOUNT_JSON:**
- Click **Secret file** (if available) or paste the JSON string
- Paste your entire `service_account.json` content as a single line

### Step 5: Create requirements.txt

If you don't have it:

```bash
pip freeze > requirements.txt
```

Add these if missing:
```
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
sendgrid==6.10.0
firebase-admin==6.2.0
google-generativeai==0.3.0
google-auth==2.25.2
PyJWT==2.8.1
youtube-transcript-api==0.6.2
```

### Step 6: Deploy

1. Push to GitHub:
   ```bash
   git push
   ```

2. Render automatically deploys on push
3. Check deployment status in Render dashboard

---

## Local Development Setup

### First Time Setup

1. **Copy template file:**
   ```bash
   cp utils/service_account.json.example utils/service_account.json
   ```

2. **Add your Firebase credentials** to `utils/service_account.json`

3. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

4. **Fill in .env:**
   ```
   SENDGRID_API_KEY=your_key
   JWT_SECRET=your_secret
   BASE_URL=http://localhost:8001
   ```

5. **Don't commit these files** (they're in .gitignore)

### Running Locally

```bash
python main.py
```

---

## File Structure (Safe for Git)

```
idk/
├── .env                              ✗ NOT in Git (in .gitignore)
├── .env.example                      ✓ Template in Git
├── utils/
│   ├── service_account.json          ✗ NOT in Git (in .gitignore)
│   ├── service_account.json.example  ✓ Template in Git
│   └── helpers.py
├── Repository/
│   ├── Firebase.py                   ✓ Loads from env or file
│   ├── sendGrid.py
│   └── Youtube.py
└── main.py
```

---

## Testing on Render

After deployment:

1. Visit: `https://your-app.onrender.com`
2. Test registration: Submit test email
3. Check Render logs:
   - Dashboard → Service → Logs
   - Look for success/error messages

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Deploy fails | Missing env vars | Check Render Environment tab |
| Firebase 403 | Invalid credentials | Verify JSON in env variable |
| SendGrid fails | API key wrong | Copy correct key from SendGrid |
| Secrets exposed | File in git | Use `git rm --cached` and add to .gitignore |

---

## Security Checklist

- [ ] `.env` in .gitignore
- [ ] `service_account.json` in .gitignore
- [ ] No API keys in code (use env vars only)
- [ ] Render has all required environment variables
- [ ] Firebase credentials stored securely
- [ ] Git history cleaned of secrets
- [ ] `git log` shows no secrets
- [ ] Production uses strong JWT_SECRET

---

## Commands Reference

```bash
# Check what will be pushed
git status

# Remove file from git (keep local copy)
git rm --cached utils/service_account.json

# Verify .gitignore is working
git check-ignore -v utils/service_account.json

# See git history
git log --oneline

# View environment in Render
render env:pull
```

---

## After Push Rejection

The error was due to secrets. Now that you've fixed it:

1. Remove the file: `git rm --cached utils/service_account.json`
2. Commit: `git commit -m "Remove secrets from git"`
3. Update .gitignore (already done above)
4. Push: `git push`

Then set up Render with environment variables as described above.
