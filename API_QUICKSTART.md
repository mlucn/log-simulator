# API Quick Start Guide

## Installation

```bash
# Install with API dependencies
pip install -e ".[api]"
```

## Start the Server

```bash
# Development mode (with auto-reload)
uvicorn log_simulator.api.main:app --reload --host 0.0.0.0 --port 8080

# Disable rate limiting for local testing
LOG_SIM_RATE_LIMIT_ENABLED=false uvicorn log_simulator.api.main:app --reload
```

## Test the API

### 1. Health Check
```bash
curl http://localhost:8080/api/v1/health | jq .
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "schemas_available": 9
}
```

### 2. List Available Schemas
```bash
curl http://localhost:8080/api/v1/schemas | jq .
```

### 3. Get Schema Details
```bash
curl http://localhost:8080/api/v1/schemas/cloud_identity/google_workspace | jq .
```

### 4. Generate Logs
```bash
curl -X POST http://localhost:8080/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "schema_name": "cloud_identity/google_workspace",
    "count": 5,
    "scenario": "user_login_success",
    "overrides": {
      "actor.email": "admin@company.com",
      "ipAddress": "10.0.1.50"
    },
    "time_spread_seconds": 300
  }' | jq .
```

## Interactive API Documentation

Visit these URLs after starting the server:

- **Swagger UI**: http://localhost:8080/api/v1/docs
- **ReDoc**: http://localhost:8080/api/v1/redoc

## Example Requests

### Generate Simple Logs
```bash
curl -X POST http://localhost:8080/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"schema_name": "web_servers/nginx_access", "count": 10}' \
  | jq '.logs[0]'
```

### Generate with Scenario
```bash
curl -X POST http://localhost:8080/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "schema_name": "security/crowdstrike_fdr",
    "count": 3,
    "scenario": "process_creation"
  }' | jq '{count: .count, execution_time: .execution_time}'
```

### Generate with Time Spread
```bash
curl -X POST http://localhost:8080/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "schema_name": "cloud_infrastructure/aws_cloudtrail",
    "count": 20,
    "time_spread_seconds": 3600
  }' | jq '.execution_time'
```

## Configuration

Set environment variables to configure the API:

```bash
# Server settings
export LOG_SIM_HOST=0.0.0.0
export LOG_SIM_PORT=8080
export LOG_SIM_DEBUG=true

# Rate limiting
export LOG_SIM_RATE_LIMIT_ENABLED=false

# Generation limits
export LOG_SIM_MAX_LOG_COUNT=50000
export LOG_SIM_MAX_TIME_SPREAD=86400

# Start server
uvicorn log_simulator.api.main:app --reload
```

## Next Steps

- See [full API documentation](docs/API.md) for detailed endpoint reference
- Check the interactive Swagger UI at `/api/v1/docs` for trying out requests
- See [Docker guide](docker/README.md) for containerized deployment (coming soon)

## Troubleshooting

**Port already in use:**
```bash
# Find and kill process using port 8080
lsof -ti:8080 | xargs kill -9

# Or use a different port
uvicorn log_simulator.api.main:app --port 8081
```

**Module not found:**
```bash
# Make sure you installed with API dependencies
pip install -e ".[api]"
```

**Schemas not found:**
```bash
# Verify schemas directory exists
ls -la src/log_simulator/schemas/
```
