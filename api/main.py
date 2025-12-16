"""FastAPI Backend for Insurance Fraud Detection

Serves predictions through a REST API endpoint.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Insurance Fraud Detection API",
    description="ML API for detecting fraudulent insurance claims",
    version="1.0.0"
)

# Add CORS middleware for Streamlit integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None

# Define request schema
class ClaimData(BaseModel):
    claim_amount: float
    claim_age: int
    claim_type: str
    claimant_age: int
    policy_duration: float
    monthly_premium: float
    witnesses: int
    police_report: int
    injury_claim: int
    property_claim: int
    vehicle_claim: int

    class Config:
        example = {
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
        }

# Define response schema
class PredictionResponse(BaseModel):
    fraud_detected: bool
    fraud_probability: float
    risk_level: str
    message: str

@app.on_event("startup")
def load_model():
    """Load the trained model on startup"""
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), "../models/fraud_detection_model.pkl")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

@app.get("/", tags=["Health Check"])
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Insurance Fraud Detection API",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health Check"])
def health_check():
    """Detailed health check with model status"""
    return {
        "status": "operational",
        "model_loaded": model is not None,
        "service": "Insurance Fraud Detection API"
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
def predict_fraud(claim: ClaimData):
    """
    Predict if an insurance claim is fraudulent.
    
    Returns:
    - fraud_detected: Boolean indicating if fraud is detected
    - fraud_probability: Confidence score (0-1)
    - risk_level: "Low", "Medium", or "High"
    - message: Human-readable explanation
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Prepare feature vector (must match training data order)
        features = np.array([[
            claim.claim_amount,
            claim.claim_age,
            claim.claimant_age,
            claim.policy_duration,
            claim.monthly_premium,
            claim.witnesses,
            claim.police_report,
            claim.injury_claim,
            claim.property_claim,
            claim.vehicle_claim,
            1 if claim.claim_type.lower() == 'auto' else 0,
            1 if claim.claim_type.lower() == 'home' else 0,
            1 if claim.claim_type.lower() == 'health' else 0,
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        fraud_detected = prediction == 1
        
        # Generate message
        if fraud_detected:
            message = f"⚠️ Fraud Alert! Confidence: {probability*100:.1f}%"
        else:
            message = f"✅ Claim appears legitimate. Confidence: {(1-probability)*100:.1f}%"
        
        return PredictionResponse(
            fraud_detected=fraud_detected,
            fraud_probability=round(probability, 4),
            risk_level=risk_level,
            message=message
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/info", tags=["Information"])
def get_info():
    """Get API information and usage"""
    return {
        "api_name": "Insurance Fraud Detection ML API",
        "version": "1.0.0",
        "description": "Detects fraudulent insurance claims using Machine Learning",
        "model_accuracy": "93%",
        "endpoints": {
            "GET /": "Health check",
            "GET /health": "Detailed health status",
            "POST /predict": "Predict fraud for a claim",
            "GET /info": "API information",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "GET /redoc": "ReDoc documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
