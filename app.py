from flask import Flask, Response, render_template, jsonify, request
import time
import os
import psutil
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
REQUEST_COUNT = Counter(
    "aegisops_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "aegisops_http_request_duration_seconds",
    "Time spent processing HTTP requests",
    ["endpoint"]
)
app = Flask(__name__)

# Remember when AegisOps started
START_TIME = time.time()

# Count how many requests AegisOps receives
request_count = 0

@app.before_request
def count_request():
    global request_count
    request_count += 1

    request.start_time = time.time()

@app.route("/test-error")
def test_error():
    return jsonify({
        "status": "error",
        "message": "Simulated server failure"
    }), 500

@app.after_request
def record_metrics(response):

    if request.path != "/metrics":

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()

        request_duration = time.time() - request.start_time

        REQUEST_LATENCY.labels(
            endpoint=request.path
        ).observe(request_duration)

    return response



@app.route("/api/status")
def status():
    uptime = int(time.time() - START_TIME)

    process = psutil.Process(os.getpid())

    return jsonify({
        "service": "AegisOps",
        "status": "operational",
        "version": "1.0.0",
        "environment": "production",
        "uptime_seconds": uptime,
        "requests": request_count,
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "process_memory_mb": round(
            process.memory_info().rss / 1024 / 1024, 2
        )
    })

@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "AegisOps",
        "version": "1.0.0"
    })

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)