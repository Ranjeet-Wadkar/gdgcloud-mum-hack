FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    gcc g++ libc6-dev libffi-dev libssl-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Cloud Run sets PORT dynamically
ENV PORT=8080

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/_stcore/health || exit 1

# Run Streamlit on Cloud Run's PORT
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
