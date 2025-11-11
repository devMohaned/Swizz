# Swizz Project — Kubernetes Deployment Guide

## Prerequisites

You’ll need the following tools installed:

- **Minikube** — [Install Guide](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download)  
- **Docker** — [Get Started](https://www.docker.com/get-started/)  
- **kubectl** — [Install Guide](https://kubernetes.io/docs/tasks/tools/)

---

## Setup Local Environment

Initialize your local cluster:

```bash
minikube start --driver=docker
kubectl config current-context   # should print "minikube"
kubectl get nodes
```

---

## Namespace and Secrets

Create a namespace for the project:

```bash
kubectl create namespace swizz
```

Create a secret file for the app:

```bash
kubectl -n swizz create secret generic app-secrets   --from-literal=DATABASE_USER=appuser   --from-literal=DATABASE_PASSWORD=apppass   --from-literal=JWT_SECRET=supersecret
```

---

## Deployments & Services

You need to create a deployment/service for each component.

### PostgreSQL

- YAML Path (Go to that directory in the command line): `{ProjectPath}\Swizz\users_service\k8s\postgres.yaml`
- Apply Command:

  ```bash
  kubectl -n swizz apply -f postgres.yaml
  ```

### Users API Service

- YAML Path (Go to that directory in the command line): `{ProjectPath}\Swizz\users_service\k8s\users-service.yaml`
- Apply Command:

  ```bash
  kubectl -n swizz apply -f users-service.yaml
  ```

### OPA Engine

- YAML Path (Go to that directory in the command line): `{ProjectPath}\Swizz\opa\k8s\opa.yaml`
- Apply Command:

  ```bash
  kubectl -n swizz apply -f opa.yaml
  ```

### OPA Service

- YAML Path (Go to that directory in the command line): `{ProjectPath}\Swizz\opa_service\k8s\opa-service.yaml`
- Apply Command:

  ```bash
  kubectl -n swizz apply -f opa-service.yaml
  ```

---

## Verify Deployment

Check that all deployments are running:

```bash
kubectl -n swizz rollout status deploy/postgres
kubectl -n swizz rollout status deploy/opa
kubectl -n swizz rollout status deploy/opa-service
kubectl -n swizz rollout status deploy/users-service
kubectl -n swizz get pods,svc
```

---

## Port Forwarding for Testing

Expose services locally for testing:

```bash
# Users API
kubectl -n swizz port-forward svc/users-service 8000:8000

# (Optional) OPA wrapper and engine
kubectl -n swizz port-forward svc/opa-service 8001:8001
kubectl -n swizz port-forward svc/opa 8181:8181
```

---

## API Testing Tokens

**Admin Token (Valid until 2030):**
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6ImFkbWluIiwiYXVkIjoidXNlcnMtYXBpIiwiaXNzIjoiYXV0aC1zZXJ2aWNlIiwiZXhwIjoxOTE4MzI5OTUxfQ.9r5qXmFikumT_sn2ChaX2F_LsjDjY3nlGBRZsUbjZOQ
```

**Authenticated Token (Non-Admin, Valid until 2030):**
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6Im5vbkFkbWluUm9sZSIsImF1ZCI6InVzZXJzLWFwaSIsImlzcyI6ImF1dGgtc2VydmljZSIsImV4cCI6MTkxODMyOTk5M30.veeHicL-Ipg1aSV5btIIaqy9c_jHpbAdbmhsedUdZCA
```

**Expired Token:**
```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6Im5vbkFkbWluUm9sZSIsImF1ZCI6InVzZXJzLWFwaSIsImlzcyI6ImF1dGgtc2VydmljZSIsImV4cCI6MTc2Mjc5MjAzNH0.3-OVprOJQVHWSoKeTfYyArfU4x03ECbDqz5wKX0dqzM
```

---

## Environment Variables

### users-service

**From Secret:**
- `DATABASE_USER`, `DATABASE_PASSWORD`, `JWT_SECRET`

**From ConfigMap:**
```
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=appdb
OPA_SERVICE_URL=http://opa-service:8001/api/internal/evaluate
TIMEOUT=5.0
APP_NAME
ENVIRONMENT
LOG_FORMAT
LOG_LEVEL
LOG_FILE_PATH
JWT_ALGORITHM=HS256
JWT_AUDIENCE=users-api
JWT_ISSUER=auth-service
```

---

### opa-service

**From ConfigMap:**
```
OPA_URL=http://opa:8181/v1/data/http/authz/allow
TIMEOUT
LOG_*
ENVIRONMENT
```

---

### postgres

**From Secret:**
- `POSTGRES_USER`, `POSTGRES_PASSWORD`

**From Environment:**
```
POSTGRES_DB=appdb
```

**PVC:**
- `postgres-pvc (1Gi)`

---

## Postman Collections

# Swiss API Collection

This Postman collection includes API endpoints for **Users Service** and **OPA Authorization** used in the Swizz project.

---

## Endpoints

### 1. Get All Users

**Method:** `GET`  
**URL:** `http://localhost:8000/api/users`

**Headers:**
| Key | Value |
|------|------|
| Authorization | Bearer *eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...* |

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/users \
  -H "Authorization: Bearer <token>"
```

---

### 2. Save a User

**Method:** `POST`  
**URL:** `http://localhost:8000/api/users`

**Headers:**
| Key | Value |
|------|------|
| Authorization | Bearer *eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...* |

**Body:**
```json
{
  "name": "hii",
  "email": "emai34@gmail.com"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "hii",
        "email": "emai34@gmail.com"
      }'
```

---

### 3. OPA Service (Internal API)

**Method:** `POST`  
**URL:** `http://localhost:8001/api/internal/evaluate`

**Headers:**
| Key | Value |
|------|------|
| Content-Type | application/json |
| X-Request-Id | ea7cbd5a-b655-4bf5-bff5-d8b08fac9111 |

**Body:**
```json
{
  "method": "POST",
  "path": "/api/users",
  "role": "admin",
  "sub": "user123",
  "request_id": "ea7cbd5a-b655-4bf5-bff5-d8b08fac9111"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8001/api/internal/evaluate \
  -H "Content-Type: application/json" \
  -d '{
        "method": "POST",
        "path": "/api/users",
        "role": "admin"
      }'
```

---

### 4. OPA Directly (Admin)

**Method:** `POST`  
**URL:** `http://localhost:8181/v1/data/http/authz/allow`

**Headers:**
| Key | Value |
|------|------|
| Content-Type | application/json |

**Body:**
```json
{
  "input": {
    "method": "GET",
    "path": "/api/users",
    "role": "admin",
    "sub": "user123"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8181/v1/data/http/authz/allow \
  -H "Content-Type: application/json" \
  -d '{"input": {"method":"POST","path":"/api/users","role":"admin"}}'
```

---

### 5. OPA Directly (Authenticated)

**Method:** `POST`  
**URL:** `http://localhost:8181/v1/data/http/authz/allow`

**Headers:**
| Key | Value |
|------|------|
| Content-Type | application/json |

**Body:**
```json
{
  "input": {
    "method": "GET",
    "path": "/api/users",
    "role": "authenticated",
    "sub": "user123"
  }
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8181/v1/data/http/authz/allow \
  -H "Content-Type: application/json" \
  -d '{"input": {"method":"POST","path":"/api/users","role":"authenticated"}}'
```

---

## Full Postman Collection (JSON)

```json
{
	"info": {
		"_postman_id": "6f3140e4-1366-4d2b-9cf5-46fad737372f",
		"name": "Swiss",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "23277089"
	},
	"item": [
		{
			"name": "Get All Users",
			"request": {
				"method": "GET",
				"header": [
					{
						"key": "Authorization",
						"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6ImFkbWluIiwiYXVkIjoidXNlcnMtYXBpIiwiaXNzIjoiYXV0aC1zZXJ2aWNlIiwiZXhwIjoxOTE4MzI5OTUxfQ.9r5qXmFikumT_sn2ChaX2F_LsjDjY3nlGBRZsUbjZOQ",
						"type": "text"
					}
				],
				"url": {
					"raw": "http://localhost:8000/api/users",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8000",
					"path": [
						"api",
						"users"
					]
				}
			},
			"response": []
		},
		{
			"name": "Save a User",
			"request": {
				"method": "POST",
				"header": [
					{
						"key": "Authorization",
						"value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6ImFkbWluIiwiYXVkIjoidXNlcnMtYXBpIiwiaXNzIjoiYXV0aC1zZXJ2aWNlIiwiZXhwIjoxOTE4MzI5OTUxfQ.9r5qXmFikumT_sn2ChaX2F_LsjDjY3nlGBRZsUbjZOQ",
						"type": "text"
					}
				],
				"body": {
					"mode": "raw",
					"raw": "{\r\n    \"name\": \"hii\",\r\n    \"email\": \"emai34@gmail.com\"\r\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "http://localhost:8000/api/users",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8000",
					"path": [
						"api",
						"users"
					]
				}
			},
			"response": []
		}
	]
}
```

---


---

## Cleanup Commands

Delete the project namespace:

```bash
kubectl delete ns swizz
```

Clean up everything in the Minikube cluster:

```bash
minikube delete --all --purge
```
