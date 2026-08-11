# AegisOps
AegisOps is a containerized web-server monitoring and observability project built for a DevOps internship task provided by CodeAlpha.

And the name itself means:

Aegis = protection/shield
Ops = operations

So AegisOps = protection for your application operations.

The project demonstrates how a web application can be deployed inside Docker, monitored for health and performance, and observed using Prometheus and Grafana.

## Tech Stack
- Python
- Flask
- Gunicorn
- Docker
- Docker Compose
- Prometheus
- Grafana
- HTML, CSS and JavaScript

## Features
- Containerized Flask web application
- Production-style Gunicorn web server
- Docker health checks
- `/health` endpoint for service monitoring
- `/metrics` endpoint for Prometheus
- HTTP request counting
- Request latency monitoring
- HTTP 5xx error monitoring
- CPU monitoring
- Memory monitoring
- Grafana observability dashboard
- Persistent Grafana storage using Docker volumes
- Controlled HTTP 500 failure testing

## Architecture
AegisOps Application
        |
        | exposes /metrics
        v
Prometheus
        |
        | queries metrics
        v
Grafana Dashboard

All services run as Docker containers using Docker Compose.

## Services
| Service | Port | Purpose |
|---|---:|---|
| AegisOps | 5000 | Web application |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Monitoring dashboard |

## Monitoring Dashboard
The Grafana dashboard monitors:

- Service health
- Requests per second
- Average request latency
- HTTP error rate
- Total HTTP requests
- CPU usage
- Memory usage

## Health Check
AegisOps exposes:
`/health`
Example response:
```json
{
  "status": "healthy",
  "service": "AegisOps",
  "version": "1.0.0"
}

Failure Simulation
For monitoring tests, AegisOps includes:
/test-error
This intentionally returns HTTP status 500.
It was used to verify that:
AegisOps → Prometheus → Grafana
can detect and visualize application failures.

Running the Project

Build and start all services:
docker compose up -d --build

Check running containers:
docker compose ps

View application logs:
docker logs aegisops-app

Stop the services:
docker compose down

Access:-

AegisOps:
http://localhost:5000

Health endpoint:
http://localhost:5000/health

Metrics:
http://localhost:5000/metrics

Prometheus:
http://localhost:9090

Grafana:
http://localhost:3000

Docker Best Practices Used
Lightweight Python slim image
.dockerignore
Dependency layer caching
--no-cache-dir for Python packages
Docker health checks
Docker Compose
Persistent named volumes
Gunicorn instead of Flask's development server
Separate monitoring services
Troubleshooting Practiced

During development, several real issues were diagnosed and fixed, including:

Docker daemon not running
Missing Python dependencies
Container health-check failures
Port conflicts
Prometheus scraping configuration
Grafana data-source configuration
PromQL query troubleshooting
HTTP 500 failure detection
Docker Compose YAML configuration errors
Persistent Grafana storage
Internship Task

This project addresses the following Docker web-server objectives:

Docker containerization basics
Deployment and management of a web server
Container lifecycle commands
Container health monitoring
Troubleshooting
Container-based deployment best practices

 Author
Khadija Azhar