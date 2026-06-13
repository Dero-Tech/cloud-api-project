from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import os
import datetime

app = Flask(__name__)

# This single line adds a /metrics endpoint and automatically
# tracks request count, latency, and errors for every route
metrics = PrometheusMetrics(app)

# Static app info — shows up as a label in your metrics
metrics.info('app_info', 'Cloud API Metrics', version='1.0.0')

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "Cloud API is running",
        "version": "1.0.0"
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "environment": os.getenv("APP_ENV", "production")
    })

@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "app": "Cloud Engineering Demo API",
        "description": "Dockerized Flask API deployed on AWS with Terraform and GitHub Actions CI/CD",
        "tech_stack": {
            "language": "Python / Flask",
            "containerization": "Docker",
            "infrastructure": "AWS (EC2, VPC, S3, Security Groups)",
            "iac": "Terraform",
            "ci_cd": "GitHub Actions",
            "observability": "Prometheus + Grafana + CloudWatch"
        },
        "author": "David"
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
