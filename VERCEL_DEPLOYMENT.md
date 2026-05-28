# ▲ Vercel Frontend Deployment Guide

This guide explains how to deploy the React frontend of MediBee using Vercel.

---

# 📌 What is Vercel?

Vercel is a cloud platform used to host frontend applications like:
- React apps
- Next.js apps
- static websites

It automatically:
- builds your frontend
- hosts it online
- redeploys every time you push to GitHub

---

# ✅ Prerequisites

Before starting, make sure you have:

- GitHub account
- Your project pushed to GitHub
- React frontend working locally

---

# 1️⃣ Push Project to GitHub

Your project should already exist on GitHub.

Example:

```text
https://github.com/NandithaNair19/MediBee
```

---

# 2️⃣ Create Vercel Account

Open:

```text
https://vercel.com/signup
```

Sign up using:
- GitHub
- OR email

Recommended:
```text
Continue with GitHub
```

---

# 3️⃣ Import GitHub Repository

After logging into Vercel:

1. Click:

```text
Add New Project
```

2. Select:

```text
Import Git Repository
```

3. Choose your repository:

```text
MediBee
```

4. Click:

```text
Import
```

---

# 4️⃣ Configure Frontend Deployment

IMPORTANT:

Since the React app is inside the `frontend` folder, configure these settings carefully.

---

## Framework Preset

Set:

```text
Create React App
```

---

## Root Directory

Set:

```text
frontend
```

This tells Vercel where the React app exists.

---

## Build Command

```text
npm run build
```

---

## Output Directory

```text
build
```

---

## Install Command

```text
npm install
```

---

# 5️⃣ Add Environment Variables 

Go to:

```text
Project Settings → Environment Variables
```

Example:

```env
REACT_APP_BACKEND_URL=https://your-render-url.onrender.com
```

---

# 6️⃣ Deploy

Click:

```text
Deploy
```

Vercel will now:
- install dependencies
- build React app
- host it online

---

# 7️⃣ Access Live Frontend

After deployment, Vercel generates a URL like:

```text
https://medi-bee.vercel.app
```

Your frontend is now live.

---

# 🔄 Automatic CI/CD

Every time you push code to GitHub:

```bash
git push
```

Vercel automatically:
- rebuilds frontend
- redeploys updated version

No manual redeployment required.

---

# 🛠️ Common Errors

## Blank Screen

Usually caused by:
- wrong backend URL
- wrong root directory
- frontend build failure

---

## Build Failed

Check:
- package.json exists inside frontend
- npm install works locally

---

## API Not Working

Make sure:
- backend is deployed
- backend CORS allows Vercel URL

Example:

```python
allow_origins=[
    "http://localhost:3000",
    "https://medi-bee.vercel.app",
]
```

---

# ✅ Final Result

You now have:
- cloud-hosted React frontend
- automatic deployment
- public sharable URL
- CI/CD pipeline connected to GitHub
