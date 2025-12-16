# Multi-stage build: FastAPI + Streamlit in one Docker image
# Stage 1: Base image with Python
FROM python:3.10-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add additional deployment dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    streamlit==1.28.1 \
    requests==2.31.0 \
    pydantic==2.5.0 \
    python-multipart==0.0.6

# Copy application code
COPY . .

# Expose ports
# 8000 for FastAPI
# 8501 for Streamlit
EXPOSE 8000 8501

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting Insurance Fraud Detection System..."\n\
echo "Starting FastAPI backend on port 8000..."\n\
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &\n\
sleep 5\n\
echo "Starting Streamlit frontend on port 8501..."\n\
streamlit run app.py --server.port=8501 --server.address=0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run startup script
CMD ["/app/start.sh"]
