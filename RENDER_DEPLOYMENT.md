# 🚀 Render Backend Deployment Guide

This guide explains how to deploy the FastAPI backend of MediBee using Render.

---

# 📌 What is Render?

Render is a cloud platform used to host backend applications like:
- FastAPI
- Flask
- Node.js
- Django
- APIs and databases

It automatically:
- deploys backend servers
- hosts APIs online
- redeploys whenever GitHub code changes

---

# ✅ Prerequisites

Before starting, make sure you have:

- GitHub account
- Backend pushed to GitHub
- FastAPI backend working locally

---

# 1️⃣ Push Project to GitHub

Your project should already exist on GitHub.

Example:

```text
https://github.com/NandithaNair19/MediBee
```

---

# 2️⃣ Create Render Account

Open:

```text
https://render.com/register
```

Sign up using:
- GitHub
- OR email

Recommended:

```text
Continue with GitHub
```

---

# 3️⃣ Create New Web Service

After logging into Render:

1. Click:

```text
New +
```

2. Select:

```text
Web Service
```

3. Connect your GitHub repository.

4. Choose:

```text
MediBee
```

5. Click:

```text
Connect
```

---

# 4️⃣ Configure Backend Deployment

IMPORTANT:

Since FastAPI exists inside the `backend` folder, configure these settings carefully.

---

# 🛠️ Basic Settings

## Name

Example:

```text
medibee
```

---

## Root Directory

Set:

```text
backend
```

---

## Runtime

Select:

```text
Python 3
```

---

## Build Command

```text
pip install -r requirements.txt
```

---

## Start Command

```text
python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

This starts the FastAPI server correctly on Render.

---

# 5️⃣ Add Environment Variables

Open:

```text
Environment → Add Environment Variable
```

Add:

| Key | Value |
|---|---|
| OPENAI_API_KEY | your_openai_key |
| GEOAPIFY_API_KEY | your_geoapify_key |

---

# 6️⃣ Deploy Backend

Click:

```text
Create Web Service
```

Render will now:
- install dependencies
- build backend
- deploy FastAPI server

Deployment may take a few minutes.

---

# 7️⃣ Access Live Backend

After deployment, Render generates a URL like:

```text
https://medibee.onrender.com
```

Opening the URL should display:

```json
{
  "message": "Medical Store Locator API is running"
}
```

---

# 🔄 Automatic CI/CD

Every time you push code to GitHub:

```bash
git push
```

Render automatically:
- redeploys backend
- updates latest API version

No manual redeployment required.

---

# 🌐 Connecting Frontend to Backend

Inside React frontend, replace local backend URL:

```javascript
http://127.0.0.1:8000
```

with deployed Render URL:

```javascript
https://your-render-url.onrender.com
```

Example:

```javascript
const response = await fetch(
  "https://medibee-uqg6.onrender.com/search-by-pincode",
```

---

# 🛠️ Common Errors

## CORS Error

Backend must allow frontend URL:

```python
allow_origins=[
    "http://localhost:3000",
    "https://medi-bee.vercel.app",
]
```

---

## Build Failed

Usually caused by:
- missing requirements.txt
- wrong root directory
- wrong start command

---

## Backend Sleeping

Free Render services may sleep after inactivity.

First request after inactivity can take:
- 30–60 seconds

This is normal for free tier hosting.

---

# ✅ Final Result

You now have:
- cloud-hosted FastAPI backend
- public API endpoint
- automatic deployment
- CI/CD pipeline connected to GitHub
- frontend + backend fully deployed
