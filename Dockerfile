FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy SDK first and install it
COPY sdk ./sdk
RUN pip install -e ./sdk --no-cache-dir --no-deps \
    && pip install \
        "fairlearn>=0.10" \
        "scikit-learn>=1.3" \
        "pandas>=2.0" \
        "numpy>=1.24" \
        "jinja2>=3.1" \
        "pyyaml>=6.0" \
        --no-cache-dir

# Copy backend files
COPY deploy/backend ./deploy/backend

# Install backend deps
RUN pip install -r ./deploy/backend/requirements.txt --no-cache-dir \
    && pip install requests --no-cache-dir

# Copy local database into expected location
COPY local_data ./deploy/backend/local_data

# Set working directory to the backend
WORKDIR /app/deploy/backend

EXPOSE 8080
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
