# 🐝 MediBee

MediBee is a modern full-stack medical store locator web application that helps users quickly find nearby pharmacies using either **text input** or **voice-based pincode detection**.

Built using **React + FastAPI**, the application supports real-time medical store search, distance calculation, Google Maps integration, CI/CD automation, and full cloud deployment.

---

# 🔗 One-Click Access

## 🌐 Live Frontend

Use the deployed MediBee application here:

https://medi-bee.vercel.app

---

## ⚙️ Live Backend API

Check the deployed FastAPI backend here:

https://medibee-uqg6.onrender.com

When opened, it should display:

```json
{
  "message": "Medical Store Locator API is running"
}
```

---

# ✨ Features

- 💊 Search nearby medical stores by pincode
- 🎤 Voice-based pincode detection
- 📍 Distance calculation from user location
- 🗺️ Google Maps integration
- 🌍 Real-time pharmacy search using Geoapify APIs
- 📱 Responsive modern UI
- ⚡ FastAPI backend APIs
- 🚀 Fully deployed frontend & backend
- 🔄 CI/CD pipeline with GitHub Actions
- 🧪 API testing using Postman
- ☁️ Vercel + Render deployment
- 📊 Backend logging and monitoring

---

# 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Frontend | React.js, CSS3, Web Speech API |
| Backend | FastAPI, Python |
| APIs | Geoapify API, OpenAI Whisper API |
| Deployment | Vercel, Render |
| CI/CD | GitHub Actions |
| Testing | Postman |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```bash
medical-store-app/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
└── .github/
    └── workflows/
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone https://github.com/NandithaNair19/MediBee.git
cd MediBee
```

---

# 🔹 Backend Setup

## Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Create `.env`

```env
OPENAI_API_KEY=your_openai_key
GEOAPIFY_API_KEY=your_geoapify_key
```

## Run Backend

```bash
python3 -m uvicorn main:app --reload
```

Backend runs at:

```bash
http://127.0.0.1:8000
```

---

# 🔹 Frontend Setup

## Install Dependencies

```bash
cd frontend
npm install
```

## Run Frontend

```bash
npm start
```

Frontend runs at:

```bash
http://localhost:3000
```

---

# 🎤 Voice Search

Users can click the microphone button and speak their pincode directly.

## Example

```text
"560103"
```

The system automatically:
- detects speech
- extracts pincode
- searches nearby pharmacies
- displays nearby medical stores

---

# 🌍 API Endpoint

## Search Medical Stores

```http
POST /search-by-pincode
```

## Request

```json
{
  "pincode": "560103",
  "user_lat": 12.9716,
  "user_lon": 77.5946
}
```

## Response

```json
{
  "stores": [
    {
      "name": "Apollo Pharmacy",
      "address": "Bangalore, Karnataka",
      "distance_km": 1.4,
      "map_link": "https://maps.google.com/..."
    }
  ]
}
```

---

# 🚀 Deployment

## Frontend
Deployed using **Vercel**

## Backend
Deployed using **Render**

## CI/CD
Every push to the `main` branch automatically:
- triggers GitHub Actions
- builds frontend
- redeploys latest version

---

# 🧪 API Testing

API endpoints were tested using **Postman** for:
- pincode search
- response validation
- error handling
- backend connectivity

---

# 📊 Monitoring & Logs

Backend logs include:
- incoming requests
- API call timings
- pharmacy search status
- response times
- error tracking

Production logs can be monitored directly from the Render dashboard.

---

# 🔮 Future Improvements

- 🌐 Multilingual voice support
- 🧠 Automatic language detection
- 📍 Live GPS-based nearby pharmacy detection
- 💬 AI chatbot assistance
- 📲 Mobile app version
- 🕒 24/7 emergency pharmacy filtering

---

# 👩‍💻 Author

Built by **Nanditha Nair**
