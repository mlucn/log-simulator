# Log Simulator API Documentation

## Overview

The Log Simulator API provides RESTful endpoints for generating synthetic log data. Built with FastAPI, it offers automatic API documentation, rate limiting, and comprehensive error handling.

## Base URL

```
http://localhost:8080/api/v1
```

## Installation

### Install API Dependencies

```bash
# Install with API support
pip install -e ".[api]"

# Or install everything
pip install -e ".[all]"
```

### Run the API Server

```bash
# Development mode (with auto-reload)
uvicorn log_simulator.api.main:app --reload --host 0.0.0.0 --port 8080

# Production mode
uvicorn log_simulator.api.main:app --host 0.0.0.0 --port 8080 --workers 4
```

## Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8080/api/v1/docs
- **ReDoc**: http://localhost:8080/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8080/api/v1/openapi.json

## Rate Limiting

To prevent abuse, the API implements rate limiting:

- **Schema endpoints**: 10 requests/minute per IP
- **Generation endpoint**: 5 requests/minute per IP

Rate limiting can be disabled for local development by setting:
```bash
export LOG_SIM_RATE_LIMIT_ENABLED=false
```

## Endpoints

### Health Check

**GET** `/health`

Check API health and availability.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "schemas_available": 9
}
```

---

### List Schemas

**GET** `/schemas`

List all available log schemas organized by category.

**Response:**
```json
{
  "schemas": {
    "cloud_identity": [
      "cloud_identity/azure_ad_signin",
      "cloud_identity/google_workspace",
      "cloud_identity/office365_audit"
    ],
    "cloud_infrastructure": [
      "cloud_infrastructure/aws_cloudtrail",
      "cloud_infrastructure/gcp_audit"
    ],
    "security": [
      "security/crowdstrike_fdr",
      "security/sysmon"
    ],
    "web_servers": [
      "web_servers/apache_access",
      "web_servers/nginx_access"
    ]
  },
  "total_count": 9
}
```

---

### Get Schema Info

**GET** `/schemas/{schema_name}`

Get detailed information about a specific schema.

**Parameters:**
- `schema_name` (path): Schema identifier (e.g., `cloud_identity/google_workspace`)

**Example:**
```bash
curl http://localhost:8080/api/v1/schemas/cloud_identity/google_workspace
```

**Response:**
```json
{
  "schema_name": "cloud_identity/google_workspace/login",
  "log_type": "WORKSPACE_ACTIVITY",
  "description": "Google Workspace login activity logs",
  "output_format": "json",
  "available_scenarios": [
    "user_login_success",
    "user_login_failure",
    "user_logout",
    "admin_action"
  ],
  "field_count": 12
}
```

---

### List Scenarios

**GET** `/schemas/{schema_name}/scenarios`

List available scenarios for a specific schema.

**Response:**
```json
{
  "schema": "cloud_identity/google_workspace",
  "scenarios": [
    "user_login_success",
    "user_login_failure",
    "user_logout",
    "admin_action"
  ]
}
```

---

### Generate Logs

**POST** `/generate`

Generate synthetic log entries based on a schema.

**Request Body:**
```json
{
  "schema_name": "cloud_identity/google_workspace",
  "count": 5,
  "scenario": "user_login_success",
  "time_spread_seconds": 300,
  "overrides": {
    "actor.email": "test@example.com",
    "ipAddress": "192.168.1.100"
  },
  "pretty": true
}
```

**Parameters:**
- `schema_name` (required): Schema to use for generation
- `count` (optional): Number of logs to generate (1-10000, default: 10)
- `scenario` (optional): Scenario name to use
- `base_time` (optional): Base timestamp (ISO 8601 format, defaults to now)
- `time_spread_seconds` (optional): Spread logs over this many seconds (0-86400)
- `overrides` (optional): Field overrides using dot notation
- `pretty` (optional): Pretty-print JSON output (default: false)

**Response:**
```json
{
  "success": true,
  "count": 5,
  "execution_time": 0.042,
  "schema_used": "cloud_identity/google_workspace",
  "scenario_used": "user_login_success",
  "logs": [
    {
      "kind": "admin#reports#activity",
      "id": {
        "time": "2025-11-16T10:30:00Z",
        "uniqueQualifier": "1234567890",
        "applicationName": "login"
      },
      "actor": {
        "email": "test@example.com"
      },
      "ipAddress": "192.168.1.100",
      "events": [
        {
          "type": "login",
          "name": "login_success"
        }
      ]
    }
  ]
}
```

---

## Usage Examples

### cURL Examples

**List all schemas:**
```bash
curl http://localhost:8080/api/v1/schemas
```

**Get schema info:**
```bash
curl http://localhost:8080/api/v1/schemas/cloud_identity/google_workspace
```

**Generate basic logs:**
```bash
curl -X POST http://localhost:8080/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "schema_name": "cloud_identity/google_workspace",
    "count": 10
  }'
```

**Generate with scenario and overrides:**
```bash
curl -X POST http://localhost:8080/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "schema_name": "security/crowdstrike_fdr",
    "count": 5,
    "scenario": "process_creation",
    "time_spread_seconds": 60,
    "overrides": {
      "ComputerName": "WORKSTATION-01",
      "UserName": "admin"
    }
  }'
```

### Python Examples

**Using requests:**
```python
import requests

# List schemas
response = requests.get("http://localhost:8080/api/v1/schemas")
schemas = response.json()
print(f"Available schemas: {schemas['total_count']}")

# Generate logs
payload = {
    "schema_name": "cloud_identity/google_workspace",
    "count": 10,
    "scenario": "user_login_success",
    "overrides": {
        "actor.email": "admin@company.com"
    }
}

response = requests.post("http://localhost:8080/api/v1/generate", json=payload)
result = response.json()

print(f"Generated {result['count']} logs in {result['execution_time']}s")
for log in result['logs']:
    print(log)
```

**Using httpx (async):**
```python
import asyncio
import httpx

async def generate_logs():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8080/api/v1/generate",
            json={
                "schema_name": "web_servers/nginx_access",
                "count": 100,
                "time_spread_seconds": 3600
            }
        )
        return response.json()

result = asyncio.run(generate_logs())
print(f"Generated {result['count']} logs")
```

## Configuration

The API can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_SIM_HOST` | `0.0.0.0` | Server host |
| `LOG_SIM_PORT` | `8080` | Server port |
| `LOG_SIM_DEBUG` | `false` | Enable debug mode |
| `LOG_SIM_RATE_LIMIT_ENABLED` | `true` | Enable rate limiting |
| `LOG_SIM_RATE_LIMIT_DEFAULT` | `10/minute` | Default rate limit |
| `LOG_SIM_RATE_LIMIT_GENERATE` | `5/minute` | Generation endpoint rate limit |
| `LOG_SIM_MAX_LOG_COUNT` | `10000` | Max logs per request |
| `LOG_SIM_MAX_TIME_SPREAD` | `86400` | Max time spread (seconds) |
| `LOG_SIM_CORS_ORIGINS` | `["*"]` | Allowed CORS origins |

**Example:**
```bash
export LOG_SIM_PORT=3000
export LOG_SIM_RATE_LIMIT_ENABLED=false
export LOG_SIM_MAX_LOG_COUNT=50000
uvicorn log_simulator.api.main:app --reload
```

## Error Responses

The API uses standard HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (schema doesn't exist)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error

**Error Response Format:**
```json
{
  "error": "Bad Request",
  "message": "Scenario 'invalid_scenario' not found in schema",
  "detail": "Available scenarios: user_login_success, user_login_failure, user_logout"
}
```

## Testing the API

**Health check:**
```bash
curl http://localhost:8080/api/v1/health
```

**Full workflow:**
```bash
# 1. List schemas
curl http://localhost:8080/api/v1/schemas | jq '.schemas'

# 2. Get schema details
curl http://localhost:8080/api/v1/schemas/cloud_identity/google_workspace | jq .

# 3. List scenarios
curl http://localhost:8080/api/v1/schemas/cloud_identity/google_workspace/scenarios | jq '.scenarios'

# 4. Generate logs
curl -X POST http://localhost:8080/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "schema_name": "cloud_identity/google_workspace",
    "count": 3,
    "scenario": "user_login_success",
    "pretty": true
  }' | jq '.logs[0]'
```

## Next Steps

- See [Docker deployment guide](../docker/README.md) for containerized deployment
- See [Cloud Run guide](../deployment/cloudrun/README.md) for cloud deployment
- Check [Frontend development](../frontend/README.md) for the web UI

## Support

- GitHub Issues: https://github.com/mlucn/log-simulator/issues
- Documentation: https://github.com/mlucn/log-simulator/docs
