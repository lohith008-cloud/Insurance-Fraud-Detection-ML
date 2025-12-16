# 🚀 ML Deployment Guide - Insurance Fraud Detection

This guide shows how to deploy your Insurance Fraud Detection ML model with **FastAPI backend + Streamlit UI**.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Deployment Architecture              │
├──────────────────────────┬──────────────────────────────┤
│  Streamlit UI (Port 8501)│     FastAPI Backend (8000)   │
│  - Web Interface         │     - ML Model Serving       │
│  - User Input Form       │     - REST API Endpoints     │
│  - Results Display       │     - Health Checks          │
└──────────────────────────┴──────────────────────────────┘
         │                             │
         └────────────┬────────────────┘
                      │
           Docker Container (Optional)
           or Cloud Deployment
```

## Quick Start (Local Development)

### Option 1: Using Docker Compose (Recommended)

**Prerequisites:**
- Docker & Docker Compose installed
- Git clone the repository

**Steps:**

1. Clone repository:
```bash
git clone https://github.com/lohith008-cloud/Insurance-Fraud-Detection-ML.git
cd Insurance-Fraud-Detection-ML
```

2. Run with Docker Compose:
```bash
docker-compose up --build
```

3. Access services:
- **Streamlit UI**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

### Option 2: Running Separately

**Install Dependencies:**
```bash
pip install -r requirements.txt
pip install fastapi uvicorn streamlit requests pydantic
```

**Terminal 1 - Start FastAPI Backend:**
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Start Streamlit UI:**
```bash
streamlit run app.py
```

## Cloud Deployment

### Deploy to Render (Recommended for Freshers)

**Step 1: Push to GitHub**
- Ensure code is on GitHub (public repo)

**Step 2: Create Render Account**
- Go to https://render.com
- Sign up with GitHub

**Step 3: Deploy Web Service**

```yaml
# Create render.yaml in root directory
services:
  - type: web
    name: insurance-fraud-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
    envVars:
      - key: PYTHON_VERSION
        value: 3.10
    
  - type: web
    name: insurance-fraud-ui
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=8501 --server.address=0.0.0.0
    envVars:
      - key: API_URL
        value: https://insurance-fraud-api.onrender.com
```

**Live Example URLs:**
- API: `https://insurance-fraud-api.onrender.com`
- UI: `https://insurance-fraud-ui.onrender.com`

### Deploy to Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Create `Procfile`:
```
api: python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
ui: streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```
5. Deploy: `railway up`

### Deploy to AWS EC2

**1. Launch EC2 Instance:**
- Ubuntu 22.04 LTS
- t3.micro (free tier eligible)
- Security Group: Allow ports 8000, 8501

**2. SSH into Instance:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

**3. Install Dependencies:**
```bash
sudo apt update
sudo apt install python3-pip docker.io
git clone https://github.com/YOUR_USERNAME/Insurance-Fraud-Detection-ML.git
cd Insurance-Fraud-Detection-ML
pip install -r requirements.txt
```

**4. Run Services:**
```bash
# Terminal 1
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# Terminal 2
streamlit run app.py
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Make Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "claim_amount": 5000,
    "claim_age": 30,
    "claim_type": "auto",
    "claimant_age": 45,
    "policy_duration": 5.0,
    "monthly_premium": 100.0,
    "witnesses": 1,
    "police_report": 1,
    "injury_claim": 0,
    "property_claim": 1,
    "vehicle_claim": 1
  }'
```

## File Structure

```
.
├── api/
│   └── main.py              # FastAPI backend
├── app.py                   # Streamlit frontend
├── Dockerfile               # Container config
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Python dependencies
├── models/
│   └── fraud_detection_model.pkl  # Trained ML model
├── src/
│   └── model.py            # Model class
└── DEPLOYMENT.md           # This file
```

## Portfolio Tips

✅ **Showcase in GitHub README:**
- Add screenshots of UI
- Link to live deployment
- Show API documentation link

✅ **Interview Talking Points:**
- "I containerized the ML model using Docker"
- "Set up a REST API with FastAPI for model serving"
- "Built interactive UI with Streamlit"
- "Deployed to cloud platform (Render/Railway/AWS)"

✅ **LinkedIn Post Template:**
```
"Just deployed my Insurance Fraud Detection ML project!

🔍 Features:
- 93% accuracy Decision Tree model
- FastAPI REST API backend
- Streamlit interactive UI
- Containerized with Docker
- Live on Render/Railway

🚀 Tech Stack: Python, FastAPI, Streamlit, Docker, Cloud

Check it out: [link]
#MachineLearning #MLOps #Deployment
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Kill process: `lsof -ti:8000` then `kill -9 PID` |
| Model not found | Ensure `models/fraud_detection_model.pkl` exists |
| API connection error | Check if backend is running on correct port |
| Streamlit cache issue | Clear: `streamlit cache clear` |

## Next Steps

1. Deploy to free cloud platform (Render/Railway)
2. Add GitHub Actions CI/CD pipeline
3. Create deployment badges in README
4. Share project link on LinkedIn
5. Document in portfolio projects

---

**Happy Deploying! 🎉**
