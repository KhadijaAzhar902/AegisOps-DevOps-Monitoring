# AegisOps

**AegisOps** is a containerized web-server monitoring and observability platform developed as part of a DevOps internship project for CodeAlpha.
The project demonstrates how a web application can be deployed inside Docker, monitored for availability and performance, tested under controlled failures, and observed through a centralized **Prometheus + Grafana monitoring stack**.
AegisOps was later extended to monitor **ReliefGrid PK**, a separate Java and Spring Boot application. This turns the project from a single-service monitoring demo into a **multi-application observability environment**.

---

## Why the Name AegisOps?

- **Aegis** = protection / shield
- **Ops** = operations

**AegisOps = protection for application operations.**

The idea behind the project is simple: an operations team should be able to see whether an application is healthy, how much traffic it is receiving, how quickly it is responding, how many failures are occurring, and how much system resource it is consuming.

---

## Project Highlights

- Containerized Flask web application
- Gunicorn production-style web server
- Docker Compose multi-container environment
- Docker health checks
- Prometheus metrics collection
- Grafana observability dashboard
- HTTP request monitoring
- Request latency monitoring
- HTTP 5xx error detection
- CPU monitoring
- Memory monitoring
- Controlled server-failure simulation
- Persistent Grafana storage
- Multi-application monitoring
- ReliefGrid Spring Boot monitoring
- JVM monitoring
- Cross-application Prometheus integration
- Real DevOps troubleshooting and debugging

---

## Tech Stack

### AegisOps Application

- Python
- Flask
- Gunicorn
- HTML
- CSS
- JavaScript

### DevOps & Observability

- Docker
- Docker Compose
- Prometheus
- Grafana
- PromQL
- Docker Volumes

### ReliefGrid Integration

- Java 21
- Spring Boot
- Gradle
- Spring Boot Actuator
- Micrometer Prometheus Registry

---

## Architecture

AegisOps originally monitored its own Flask application:

```
AegisOps Flask Application
          |
          | /metrics
          v
      Prometheus
          |
          v
        Grafana
```

The project was later extended to include ReliefGrid PK.

### Current Multi-Application Architecture

```
        AegisOps
     Python + Flask
          |
          | /metrics
          v
      Prometheus
          ^
          |
          | /actuator/prometheus
          |
     ReliefGrid PK
  Java + Spring Boot

          |
          v
       Grafana
          |
          v
AegisOps Observability Dashboard
```

Prometheus acts as the central metrics collector while Grafana provides the visualization layer.

---

## Services

| Service | Port | Purpose |
|---|---:|---|
| AegisOps | 5000 | Flask web application |
| ReliefGrid | 8080 | Java/Spring Boot application |
| Prometheus | 9090 | Metrics collection and querying |
| Grafana | 3000 | Monitoring and visualization |

---

## AegisOps Application

The Flask application exposes endpoints used for service monitoring and controlled testing.

### Main Application

```
http://localhost:5000
```

### Health Endpoint

```
http://localhost:5000/health
```

Example response:

```json
{
  "status": "healthy",
  "service": "AegisOps",
  "version": "1.0.0"
}
```

The health endpoint is also used by the Docker health check.

### Prometheus Metrics Endpoint

```
http://localhost:5000/metrics
```

Prometheus regularly scrapes this endpoint and stores the collected time-series metrics.

---

## Custom Prometheus Metrics

AegisOps defines custom metrics for HTTP traffic and application performance.

### HTTP Request Counter

```
aegisops_http_requests_total
```

Tracks HTTP requests by:

- Method
- Endpoint
- HTTP status code

### Request Duration

```
aegisops_http_request_duration_seconds
```

Measures how long requests take to process.

These metrics allow Grafana to visualize traffic, latency, and application failures.

---

## Controlled Failure Simulation

AegisOps includes a dedicated test endpoint:

```
/test-error
```

Opening this endpoint intentionally generates an:

```
HTTP 500 Internal Server Error
```

This was created to verify that the monitoring pipeline can detect application failures.

### Failure Detection Flow

```
/test-error
     |
     v
HTTP 500 generated
     |
     v
Prometheus metric updated
     |
     v
Prometheus scrapes metric
     |
     v
Grafana displays error spike
```

This provides a controlled way to test observability without intentionally breaking the actual application.

---

## Prometheus

Prometheus is responsible for collecting metrics from monitored applications.

The configuration is stored in:

```
monitoring/prometheus.yml
```

The current monitoring configuration contains separate jobs for AegisOps and ReliefGrid.

```yaml
global:
  scrape_interval: 5s

scrape_configs:

  - job_name: "aegisops"
    static_configs:
      - targets:
          - "host.docker.internal:5000"

  - job_name: "reliefgrid"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets:
          - "host.docker.internal:8080"
```

`host.docker.internal` allows the Prometheus container running in Docker Desktop to communicate with applications exposed through the host machine.

---

## Grafana Observability Dashboard

Grafana provides the visualization layer for the project.

The main dashboard is:

**AegisOps Observability Dashboard**

The exported dashboard configuration is stored as:

```
aegisops-grafana-dashboard.json
```

This allows the monitoring dashboard to be imported into another Grafana instance.

---

## AegisOps Monitoring Panels

### Service Status

Shows whether Prometheus can currently reach the AegisOps application.

```promql
up{job="aegisops"}
```

### Total HTTP Requests

```promql
sum(aegisops_http_requests_total)
```

### Requests per Second

```promql
sum(rate(aegisops_http_requests_total[1m]))
```

### Average Request Latency

```promql
(
  sum(rate(aegisops_http_request_duration_seconds_sum[1m]))
  /
  sum(rate(aegisops_http_request_duration_seconds_count[1m]))
) * 1000
```

Displayed in milliseconds.

### HTTP Error Rate

```promql
sum(
  rate(
    aegisops_http_requests_total{status=~"5.."}[1m]
  )
) or vector(0)
```

### CPU Usage

```promql
rate(process_cpu_seconds_total{job="aegisops"}[1m]) * 100
```

### Memory Usage

```promql
process_resident_memory_bytes{job="aegisops"} / 1024 / 1024
```

---

# ReliefGrid PK Integration

AegisOps was extended to monitor **ReliefGrid PK**, another DevOps internship project built using Java, Spring Boot and Gradle.

ReliefGrid is a community emergency-response application that supports:

- Incident reporting
- Incident tracking
- Community confirmations
- Severity management
- Incident status updates
- Persistent database storage
- REST APIs
- Gradle build automation
- Docker containerization
- GitHub Actions CI/CD

ReliefGrid repository:

**https://github.com/KhadijaAzhar902/ReliefGrid-PK**

---

## How ReliefGrid Exposes Metrics

ReliefGrid uses:

- Spring Boot Actuator
- Micrometer
- Prometheus Registry

Its Prometheus metrics are exposed through:

```
http://localhost:8080/actuator/prometheus
```

Prometheus scrapes the endpoint using the job:

```
job="reliefgrid"
```

The Prometheus Targets page can verify that both applications are reachable:

```
aegisops     UP
reliefgrid   UP
```

---

## ReliefGrid Monitoring Panels

### ReliefGrid Service Status

Checks whether the ReliefGrid service is currently reachable.

```promql
up{job="reliefgrid"}
```

Grafana value mapping is used to display:

```
1 = Healthy
0 = Down
```

### ReliefGrid Request Rate

Tracks recent HTTP traffic processed by Spring Boot.

```promql
sum(
  rate(
    http_server_requests_seconds_count{job="reliefgrid"}[1m]
  )
)
```

### ReliefGrid JVM Memory Usage

Tracks memory used by the Java Virtual Machine.

```promql
sum(jvm_memory_used_bytes{job="reliefgrid"}) / 1024 / 1024
```

The value is displayed in megabytes.

---

## Cross-Application Observability

The ReliefGrid integration demonstrates that AegisOps is not limited to monitoring one programming language or application.

```
Python / Flask
      |
      v
  Prometheus
      ^
      |
Java / Spring Boot
      |
      v
    Grafana
```

A Python application and a Java application can both expose metrics that are collected and visualized through the same monitoring infrastructure.

This turns AegisOps into a small **centralized observability platform** rather than only a Flask monitoring demo.

---

## Docker Architecture

AegisOps uses Docker Compose to manage its main services:

```
aegisops-app
aegisops-prometheus
aegisops-grafana
```

Ports:

```
AegisOps     -> 5000
Prometheus   -> 9090
Grafana      -> 3000
ReliefGrid   -> 8080
```

ReliefGrid can run separately while still being monitored through the same Prometheus instance.

---

## Dockerfile

The AegisOps Docker image uses a lightweight Python base image and Gunicorn for production-style application serving.

The container includes:

- Flask application
- Python dependencies
- Gunicorn
- Docker health check
- Port 5000 exposure

Gunicorn is used instead of Flask's built-in development server.

---

## Docker Health Check

The Docker image regularly checks:

```
http://127.0.0.1:5000/health
```

Docker can therefore report the AegisOps container as:

```
healthy
```

or:

```
unhealthy
```

depending on whether the application responds successfully.

---

## Persistent Grafana Storage

Grafana data is stored using a named Docker volume.

This prevents dashboards and configuration from disappearing when the Grafana container is recreated.

The persistent volume stores:

- Dashboards
- Data sources
- Grafana configuration
- User configuration

---

## Running the Project

### Build and Start

```bash
docker compose up -d --build
```

### Check Running Containers

```bash
docker compose ps
```

or:

```bash
docker ps
```

### View AegisOps Logs

```bash
docker logs aegisops-app
```

### Restart Prometheus

After changing `monitoring/prometheus.yml`:

```bash
docker compose restart prometheus
```

### Stop Services

```bash
docker compose down
```

Avoid using:

```bash
docker compose down -v
```

unless you intentionally want to remove persistent Docker volumes.

---

## Access URLs

| Service | URL |
|---|---|
| AegisOps | http://localhost:5000 |
| AegisOps Health | http://localhost:5000/health |
| AegisOps Metrics | http://localhost:5000/metrics |
| Prometheus | http://localhost:9090 |
| Prometheus Targets | http://localhost:9090/targets |
| Grafana | http://localhost:3000 |
| ReliefGrid | http://localhost:8080 |
| ReliefGrid Metrics | http://localhost:8080/actuator/prometheus |

---

## Docker Best Practices Used

- Lightweight Python base image
- `.dockerignore`
- Dependency layer caching
- `pip --no-cache-dir`
- Gunicorn production-style server
- Docker health checks
- Docker Compose
- Separate monitoring services
- Persistent named volumes
- Explicit port mappings
- External Prometheus configuration
- Application health endpoints

---

## Troubleshooting Practiced

A major part of this project involved diagnosing real DevOps problems rather than only writing application code.

Issues investigated and resolved include:

- Docker daemon not running
- Missing Python dependencies
- Missing Prometheus dependencies
- Container health-check failures
- Port conflicts
- Multiple stale processes
- Prometheus target showing `DOWN`
- Prometheus queries returning no data
- Incorrect scrape targets
- Grafana data-source configuration problems
- PromQL query troubleshooting
- HTTP 500 error detection
- Docker Compose YAML problems
- Persistent Grafana storage
- Grafana absolute vs relative time ranges
- Docker container recreation
- Docker network hostname issues
- Old Docker Compose project references
- Outdated Docker bind mounts
- Prometheus loading configuration from an older project directory
- Connecting Dockerized Prometheus to host applications
- Recreating Prometheus while preserving the remaining monitoring stack

---

## Important Troubleshooting Example: Old Prometheus Bind Mount

During development, the AegisOps project folder was moved from an older development directory to:

```
AegisOps Project
```

The existing Prometheus container was still mounted to the previous project's `prometheus.yml`.

This meant that changing the current configuration did not affect Prometheus, even after restarting the container.

The issue was diagnosed using:

```bash
docker inspect aegisops-prometheus
```

The inspection showed that Prometheus was reading configuration from the old folder.

The Prometheus container was removed and recreated using the current Docker Compose project.

After recreation, its bind mount correctly pointed to:

```
AegisOps Project/monitoring/prometheus.yml
```

ReliefGrid then appeared successfully as a Prometheus target.

This was an important practical lesson:

> Restarting a container does not change an existing bind mount. The container may need to be recreated when its mounted source path changes.

---

## Monitoring Workflow

### AegisOps

```
Application Request
        |
        v
AegisOps generates metrics
        |
        v
Prometheus scrapes /metrics
        |
        v
Prometheus stores time-series data
        |
        v
Grafana queries Prometheus
        |
        v
Dashboard visualizes application behavior
```

### Controlled Error Monitoring

```
/test-error
      |
      v
HTTP 500
      |
      v
Prometheus metric
      |
      v
Grafana error-rate spike
```

### ReliefGrid Monitoring

```
ReliefGrid Request
       |
       v
Spring Boot Actuator
       |
       v
Micrometer Metrics
       |
       v
Prometheus
       |
       v
Grafana
       |
       v
AegisOps Observability Dashboard
```

---

## Real-World Use Case

A monitoring platform like AegisOps can help during periods of heavy application traffic.

For example, during a high-traffic e-commerce sale, an operations team could monitor:

- Request volume
- Request latency
- HTTP failures
- CPU usage
- Memory usage
- Service availability

Instead of only knowing that a website is slow or unavailable, observability provides information that helps identify **why** the problem is happening.

The ReliefGrid integration demonstrates another use case: monitoring the availability and resource usage of an emergency-response application where service reliability can be particularly important.

---

## Project Structure

```
AegisOps Project
│
├── monitoring
│   └── prometheus.yml
│
├── screenshots
│
├── static
│   ├── dashboard.js
│   └── style.css
│
├── templates
│   └── dashboard.html
│
├── app.py
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── .gitignore
├── aegisops-grafana-dashboard.json
└── README.md
```

---

## Internship Task Alignment

AegisOps was originally developed for the **Web Server using Docker** internship task.

### Docker Containerization Basics

The Flask application is packaged inside a Docker image and executed as a container.

### Deploy and Manage a Web Server

Gunicorn serves the Flask application from inside Docker.

### Container Lifecycle Commands

The project uses commands including:

```bash
docker build
docker run
docker ps
docker logs
docker stop
docker start
docker inspect
docker compose up
docker compose down
docker compose restart
```

### Monitor Container Health

Docker health checks and the `/health` endpoint provide service-health visibility.

### Troubleshoot Containers

Real container, network, configuration, port, dependency, monitoring, and storage issues were diagnosed during development.

### Deployment Best Practices

The project uses:

- Docker Compose
- Gunicorn
- Health checks
- Persistent storage
- `.dockerignore`
- Separate monitoring services
- Centralized observability

---

## Extended DevOps Integration

Beyond the original Docker task, AegisOps now acts as the observability platform for another internship project:

**ReliefGrid PK — Java Application using Gradle**

```
ReliefGrid PK
Java + Spring Boot + Gradle
          |
          | application metrics
          v
       AegisOps
Prometheus + Grafana + Docker
          |
          v
 Operational Monitoring
```

Together, the two projects demonstrate:

- Gradle build automation
- Dependency management
- CI/CD
- Docker containerization
- Health checking
- Metrics collection
- Prometheus
- Grafana
- JVM monitoring
- Application observability
- Cross-project integration
- DevOps troubleshooting

---

## Screenshots

Project evidence is stored inside:

```
screenshots/
```

The screenshots demonstrate:

- AegisOps web dashboard
- Docker containers running
- Health endpoint
- Prometheus monitoring
- Grafana observability dashboard
- HTTP 500 failure detection
- ReliefGrid monitoring integration

The final integration demonstrates both AegisOps and ReliefGrid being monitored through the same observability environment.

---

## Future Improvements

Possible future improvements include:

- Prometheus Alertmanager
- Email or Slack notifications
- HTTP 5xx threshold alerts
- CPU and memory alerts
- Additional ReliefGrid JVM metrics
- ReliefGrid API latency monitoring
- Fully Dockerized ReliefGrid integration
- Kubernetes deployment
- Cloud deployment
- Centralized logging
- Longer-term metrics storage
- Additional monitored applications

---

## Author

**Khadija Azhar**
DevOps Internship Project

---

## Related Project

### ReliefGrid PK

Community emergency-response platform built with:

- Java 21
- Spring Boot
- Gradle
- Docker
- GitHub Actions CI/CD
- Spring Boot Actuator
- Prometheus
- Grafana integration

Repository:

**https://github.com/KhadijaAzhar902/ReliefGrid-PK**
