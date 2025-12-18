# 🚀 Job Alerts

![Job Alerts Bot Architecture](https://firebasestorage.googleapis.com/v0/b/cloud0924.appspot.com/o/github_images%2FJob_Alerts_Bot_Architecture.png?alt=media&token=8f7f9aec-b484-4b2b-8388-58cd2dc0000c)


## Overview

**Job Alerts** is an AI-powered job and internship notification system that automatically extracts job openings from YouTube videos and sends them to subscribed users via email. Built with FastAPI, Gemini AI, and Firebase.

Never miss a job opportunity again. Subscribe to get curated job alerts delivered directly to your inbox!

---

## 🎯 Core Features

- **🤖 AI-Powered Job Extraction**: Uses Google's Gemini AI to intelligently extract job openings from YouTube video titles, descriptions, and transcripts
- **📧 Email Notifications**: Automated job alert emails sent every 6 hours via SendGrid
- **✅ Email Verification**: Secure subscription verification with JWT tokens
- **🔄 Re-subscription**: Users can easily re-activate subscriptions after unsubscribing
- **🔐 Cron Automation**: GitHub Actions scheduled cron job runs every 6 hours
- **🎓 Smart Filtering**: Only accepts verified Gmail and university email addresses
- **📱 Responsive UI**: Clean, modern web interface for subscription management
- **🗄️ Firestore State Management**: Tracks processed videos to prevent duplicate emails

---

## ⚙️ Installation

### **Prerequisites**
- Python 3.13+
- Git
- Google Cloud APIs enabled (YouTube API v3, Gemini AI)
- SendGrid account with verified sender email
- Firebase project with Firestore database
- GitHub account (for Actions automation)

### **Local Setup**

1. **Clone Repository**
   ```bash
   git clone https://github.com/YuvaSriSai18/Job-Alerts-Bot.git
   cd Job-Alerts-Bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Fill in your credentials:
   ```env
   GCP_API_KEY=your_youtube_api_key
   GEMINI_API_KEY=your_gemini_api_key
   SENDGRID_API_KEY=your_sendgrid_api_key
   JWT_SECRET=your_secret_key
   CRON_SECRET=your_cron_secret
   BASE_URL=http://localhost:8001
   ```

4. **Generate CRON_SECRET**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Setup Firebase**
   - Download service account JSON from Firebase Console
   - Place in `utils/service_account.json` or set `FIREBASE_SERVICE_ACCOUNT_JSON` env var

6. **Run Server**
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```
   Server runs on: `http://localhost:8001`

### **Deployment (Render/Railway)**

1. **Connect GitHub Repository**
   - Link your repo to Render or Railway

2. **Set Environment Variables**
   - Add all required keys from `.env.example`

3. **Deploy**
   - Platform automatically detects `requirements.txt` and deploys
   - Service runs on provided URL

4. **Setup GitHub Actions**
   - Add `BACKEND_URL` and `CRON_SECRET` to GitHub Secrets
   - Workflow triggers automatically every 6 hours

---

## 📚 Project Structure

```
idk/
├── main.py                              # FastAPI application
├── requirements.txt                     # Python dependencies
├── .env.example                         # Environment template
├── Repository/
│   ├── Youtube.py                      # YouTube API & Gemini integration
│   ├── Firebase.py                     # Firestore database operations
│   └── sendGrid.py                     # Email service
├── utils/
│   └── helpers.py                      # JWT tokens, email validation
├── templates/
│   ├── index.html                      # Subscribe form
│   ├── resubscribe.html                # Re-subscribe form
│   ├── verify_subscription.html        # Verification page
│   ├── subscription_confirmed.html     # Success page
│   └── unsubscribe.html                # Unsubscribe confirmation
├── .github/
│   └── workflows/
│       └── job-alert-cron.yml          # GitHub Actions cron workflow
└── README.md                            # This file
```

---

## 🔗 API Endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page with subscription form |
| `/resubscribe` | GET | Re-subscribe form |
| `/register` | POST | Register new subscriber |
| `/resubscribe` | POST | Re-activate subscription |
| `/verify-email/{token}` | GET | Verify email and activate |
| `/unsubscribe/{token}` | GET | Unsubscribe from alerts |
| `/api/cron/job-alert` | GET | Cron endpoint (internal) |

---

## 📧 How It Works

1. **User Subscribes** → Enters email on homepage
2. **Verification Email** → Receives confirmation link
3. **Email Verified** → Subscription activated
4. **Cron Job Runs** (every 6 hours) → Fetches YouTube videos
5. **AI Extracts Jobs** → Gemini analyzes content
6. **Emails Sent** → Job alerts delivered to subscribers
7. **User Unsubscribes** → Can re-subscribe anytime

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Database**: Firebase Firestore
- **AI/ML**: Google Gemini 2.5-flash
- **APIs**: YouTube Data API v3
- **Email**: SendGrid
- **Authentication**: JWT (PyJWT)
- **Cron**: GitHub Actions
- **Frontend**: HTML5, Vanilla JavaScript
- **Templates**: Jinja2

---

## 📄 License

This project is open source and available under the MIT License.

---

## 💖 Made With Love

Built with ❤️ to help students and job seekers find their dream opportunities. 

**Contribute**, **Star**, and **Share** to help others! 🌟

---

**Questions?** Open an issue on GitHub or check the documentation files in the repository.