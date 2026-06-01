# Cloud Engineering Demo API

![CI/CD](https://github.com/YOUR_USERNAME/cloud-api-project/actions/workflows/ci-cd.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-containerized-2496ED?logo=docker)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20VPC%20%7C%20S3-FF9900?logo=amazonaws)

A production-style REST API demonstrating cloud engineering fundamentals:
**containerization**, **AWS infrastructure**, **Infrastructure as Code**, and **CI/CD automation**.

---

## Architecture

```
                        ┌─────────────────────────────────────────┐
                        │              AWS Cloud (us-east-1)       │
                        │                                          │
  Internet              │   ┌──────────────────────────────────┐   │
     │                  │   │          VPC (10.0.0.0/16)       │   │
     ▼                  │   │                                  │   │
┌─────────┐             │   │  ┌──────────┐   ┌───────────┐   │   │
│  Users  │────HTTP────►│   │  │ Subnet A │   │ Subnet B  │   │   │
└─────────┘             │   │  │ (AZ: a)  │   │ (AZ: b)   │   │   │
                        │   │  └────┬─────┘   └─────┬─────┘   │   │
                        │   │       │               │          │   │
                        │   │  ┌────▼───────────────▼─────┐   │   │
                        │   │  │   Application Load Balancer│  │   │
                        │   │  └────┬───────────────┬──────┘   │   │
                        │   │       │               │          │   │
                        │   │  ┌────▼────┐   ┌─────▼────┐     │   │
                        │   │  │  EC2 A  │   │  EC2 B   │     │   │
                        │   │  │ Docker  │   │  Docker  │     │   │
                        │   │  │  Flask  │   │  Flask   │     │   │
                        │   │  └─────────┘   └──────────┘     │   │
                        │   │                                  │   │
                        │   │  ┌──────────┐                   │   │
                        │   │  │ S3 Bucket│  (assets/logs)    │   │
                        │   │  └──────────┘                   │   │
                        │   └──────────────────────────────────┘   │
                        └─────────────────────────────────────────┘
```

### CI/CD Pipeline (GitHub Actions)

```
  Push to main
       │
       ▼
  ┌─────────┐     fail
  │  Tests  │──────────► ✗ Pipeline stops
  └────┬────┘
       │ pass
       ▼
  ┌─────────────┐
  │ Docker build│
  │  & push to  │
  │    GHCR     │
  └──────┬──────┘
         │
         ▼
  ┌──────────────┐
  │Manual approval│  ◄── Production gate
  └──────┬───────┘
         │ approved
         ▼
  ┌─────────────────┐
  │  Deploy to EC2  │
  │   via AWS SSM   │
  └─────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Application | Python 3.12 / Flask |
| Containerization | Docker + Docker Compose |
| Infrastructure | AWS EC2, VPC, ALB, S3, IAM |
| IaC | Terraform >= 1.5 |
| CI/CD | GitHub Actions |
| State management | Terraform remote state (S3 + DynamoDB) |
| Deployment | AWS SSM (no SSH keys required) |

---

## Project Structure

```
cloud-api-project/
├── app/
│   ├── app.py              # Flask application
│   ├── test_app.py         # Pytest test suite
│   └── requirements.txt
├── terraform/
│   ├── main.tf             # VPC, EC2, ALB, S3, IAM resources
│   ├── variables.tf        # Input variables
│   ├── outputs.tf          # Output values
│   └── templates/
│       └── user_data.sh    # EC2 bootstrap script
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # GitHub Actions pipeline
├── Dockerfile
├── docker-compose.yml      # Local development
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root — confirms API is running |
| GET | `/health` | Health check (used by ALB) |
| GET | `/info` | App info and tech stack |

---

## Local Development

**Prerequisites:** Docker, Python 3.12+

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/cloud-api-project.git
cd cloud-api-project

# Run with Docker Compose
docker-compose up

# Or run locally
pip install -r app/requirements.txt
python app/app.py

# Run tests
pytest app/test_app.py -v
```

API will be available at `http://localhost:5000`

---

## Infrastructure Deployment

**Prerequisites:** AWS CLI configured, Terraform >= 1.5

```bash
cd terraform

# Initialize Terraform (downloads AWS provider)
terraform init

# Preview what will be created
terraform plan

# Deploy infrastructure (~3 min)
terraform apply

# Tear down when done (avoids AWS charges)
terraform destroy
```

**Resources created:**
- 1 VPC with 2 public subnets across 2 availability zones
- 1 Application Load Balancer
- 2 EC2 t2.micro instances running the Docker container
- 1 S3 bucket with versioning and encryption
- IAM role + instance profile for SSM access
- Security groups with least-privilege rules

---

## CI/CD Setup

Add these secrets to your GitHub repository (`Settings → Secrets`):

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `EC2_INSTANCE_IDS` | Space-separated EC2 instance IDs from Terraform output |

The pipeline runs automatically on every push to `main`. Deployments to production require manual approval via GitHub's environment protection rules.

---

## Key Concepts Demonstrated

- **Infrastructure as Code** — all AWS resources defined in Terraform, versioned alongside application code
- **Immutable deployments** — new Docker image built and pushed on every merge; EC2 pulls the new image
- **High availability** — two EC2 instances across two availability zones behind a load balancer
- **Security best practices** — least-privilege IAM, SSM instead of SSH, S3 encryption at rest, security groups restrict EC2 to ALB traffic only
- **Production gate** — manual approval step prevents automatic deploys to production
- **Health checks** — ALB uses `/health` endpoint to route traffic only to healthy instances

---

## License

MIT
