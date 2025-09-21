# Docker Deployment Guide

This guide explains how to deploy the Research-to-Startup AI Agent Swarm using Docker.

## 🐳 Quick Start with Docker

### Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier management)
- Git (to clone the repository)

### 1. Clone and Navigate to Project

```bash
git clone <your-repo-url>
cd gdgcloud-mum-hack
```

### 2. Environment Setup

Copy the example environment file and configure your API keys:

```bash
cp env.example .env
```

Edit `.env` file with your actual API keys:

```bash
# Required for full AI functionality
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODE=production

# Optional for enhanced market research
TAVILY_API_KEY=your_actual_tavily_api_key_here
TAVILY_MODE=production
```

### 3. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up --build

# Run in detached mode (background)
docker-compose up -d --build
```

The application will be available at: `http://localhost:8501`

### 4. Alternative: Direct Docker Commands

```bash
# Build the Docker image
docker build -t research-to-startup-ai .

# Run the container
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_api_key_here \
  -e GEMINI_MODE=production \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/data:/app/data \
  research-to-startup-ai
```

## 🔧 Configuration Options

### Environment Variables

| Variable                | Default                | Description                             |
| ----------------------- | ---------------------- | --------------------------------------- |
| `GEMINI_API_KEY`        | `demo-key-placeholder` | Google Gemini API key for AI processing |
| `GEMINI_MODE`           | `demo`                 | AI mode: `demo` or `production`         |
| `TAVILY_API_KEY`        | `demo-key-placeholder` | Tavily API key for market research      |
| `TAVILY_MODE`           | `demo`                 | Tavily mode: `demo` or `production`     |
| `STREAMLIT_SERVER_PORT` | `8501`                 | Port for the Streamlit application      |
| `MAX_TEXT_LENGTH`       | `10000`                | Maximum text length for processing      |
| `MAX_PDF_PAGES`         | `50`                   | Maximum PDF pages to process            |

### Volume Mounts

- `./output:/app/output` - Persists generated pitch decks and reports
- `./data:/app/data` - Mounts investor database and other data files

## 🚀 Production Deployment

### Using Docker Compose

1. **Configure Environment Variables**

   ```bash
   # Create production .env file
   cp env.example .env.production
   # Edit with production values
   ```

2. **Deploy with Production Configuration**
   ```bash
   docker-compose --env-file .env.production up -d
   ```

### Using Docker Swarm

```bash
# Initialize swarm (if not already done)
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml research-ai
```

### Using Kubernetes

Create a Kubernetes deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: research-to-startup-ai
spec:
  replicas: 2
  selector:
    matchLabels:
      app: research-to-startup-ai
  template:
    metadata:
      labels:
        app: research-to-startup-ai
    spec:
      containers:
        - name: research-to-startup-ai
          image: research-to-startup-ai:latest
          ports:
            - containerPort: 8501
          env:
            - name: GEMINI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: gemini-api-key
            - name: GEMINI_MODE
              value: "production"
          volumeMounts:
            - name: output-volume
              mountPath: /app/output
      volumes:
        - name: output-volume
          persistentVolumeClaim:
            claimName: output-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: research-to-startup-ai-service
spec:
  selector:
    app: research-to-startup-ai
  ports:
    - port: 80
      targetPort: 8501
  type: LoadBalancer
```

## 🔍 Monitoring and Logs

### View Logs

```bash
# Docker Compose logs
docker-compose logs -f

# Docker container logs
docker logs -f research-to-startup-ai
```

### Health Checks

The container includes health checks that monitor the Streamlit application:

```bash
# Check container health
docker ps
# Look for "healthy" status

# Manual health check
curl http://localhost:8501/_stcore/health
```

## 🛠️ Development

### Development Mode

For development with live code reloading:

```bash
# Mount source code as volume for live updates
docker run -p 8501:8501 \
  -v $(pwd):/app \
  -e GEMINI_API_KEY=your_key \
  research-to-startup-ai
```

### Debugging

```bash
# Run container in interactive mode
docker run -it --entrypoint /bin/bash research-to-startup-ai

# Check container internals
docker exec -it research-to-startup-ai /bin/bash
```

## 🔒 Security Considerations

### API Key Security

- Never commit API keys to version control
- Use environment variables or Docker secrets
- Rotate API keys regularly
- Use least-privilege access

### Container Security

- The Dockerfile creates a non-root user for security
- Regular security updates for base images
- Scan images for vulnerabilities:
  ```bash
  docker scan research-to-startup-ai
  ```

## 📊 Performance Optimization

### Resource Limits

Add resource limits to docker-compose.yml:

```yaml
services:
  research-to-startup-app:
    # ... existing configuration
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 2G
        reservations:
          cpus: "0.5"
          memory: 1G
```

### Scaling

```bash
# Scale to multiple instances
docker-compose up --scale research-to-startup-app=3
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**

   ```bash
   # Change port in docker-compose.yml or kill existing process
   lsof -ti:8501 | xargs kill -9
   ```

2. **Permission Issues with Volumes**

   ```bash
   # Fix ownership
   sudo chown -R $USER:$USER ./output
   ```

3. **API Key Not Working**

   - Verify API key is correct
   - Check environment variable is set
   - Ensure API key has proper permissions

4. **Container Won't Start**
   ```bash
   # Check logs for errors
   docker-compose logs research-to-startup-app
   ```

### Getting Help

- Check application logs: `docker-compose logs -f`
- Verify environment variables: `docker-compose config`
- Test API connectivity from within container
- Check resource usage: `docker stats`

## 📝 Additional Notes

- The application works in demo mode without API keys
- Generated files are saved to the `./output` directory
- The container includes all necessary dependencies
- Health checks ensure the application is running properly
- The application is optimized for production deployment

For more information, see the main [README.md](README.md) file.
