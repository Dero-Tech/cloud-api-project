from flask import Flask, jsonify
import os
import datetime

app = Flask(__name__)

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
            "ci_cd": "GitHub Actions"
        },
        "author": "David"
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
