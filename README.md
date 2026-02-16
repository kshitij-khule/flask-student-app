# 🎓 Student Management System

A full-stack student management API built to learn real-world backend and DevOps practices — from a basic Flask app to a containerised, CI/CD-deployed cloud application.

[![Flask](https://img.shields.io/badge/Flask-3.1-blue?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?logo=docker)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20S3%20%7C%20ALB-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.11-green?logo=python)](https://www.python.org/)

---

## 🎯 About

This project started as a simple Flask app deployed manually on EC2. It's being progressively rebuilt to follow real engineering practices — proper project structure, containerisation with Docker, a real database, authentication, and an automated CI/CD pipeline.

The goal is not just a working app, but understanding *why* each piece exists.

---

## 🏗️ Architecture

```
User → S3 (Frontend) → ALB (Load Balancer) → EC2 (Docker Container → Flask API → PostgreSQL)
```

**Current State:**
```
Browser → Flask API (Docker) → SQLite
```

**Target State:**
```
Browser → S3 (HTML/JS) → ALB → EC2 (Docker) → Flask API → PostgreSQL (Docker)
                                                    ↑
                                             GitHub Actions CI/CD
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-CORS |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Auth | JWT (in progress) |
| Containerisation | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2, S3, ALB, Security Groups |

---

## 📁 Project Structure

```
flask-playground/
├── backend/
│   ├── app/
│   │   ├── __init__.py        # App factory — creates and configures Flask app
│   │   ├── config.py          # All configuration and environment variables
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── students.py    # /students endpoints
│   │   └── models/
│   │       └── __init__.py    # Database models (PostgreSQL coming soon)
│   ├── run.py                 # Entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   └── index.html
├── docker-compose.yml         # coming soon
├── .github/
│   └── workflows/
│       └── ci.yml             # coming soon
├── .gitignore
└── README.md
```

---

## 🚀 Running Locally

### With Docker (recommended)

```bash
# Clone the repo
git clone https://github.com/kshitij-khule/flask-playground.git
cd flask-playground/backend

# Create data directory and set permissions
mkdir -p data
chmod 777 data

# Create .env file
cp .env.example .env

# Build and run
docker build -t student-app .
docker run -p 5000:5000 -v $(pwd)/data:/app/data --env-file .env student-app
```

### Without Docker

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Test the API

```bash
# Health check
curl http://localhost:5000/

# Add a student
curl -X POST http://localhost:5000/students/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Kshitij", "age": 21}'

# Get all students
curl http://localhost:5000/students/
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/students/` | Get all students |
| POST | `/students/` | Add a new student |

---

## ⚙️ Environment Variables

Create a `.env` file in the `backend/` directory:

```env
DATABASE_PATH=data/students.db
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:5500
```

> `.env` is in `.gitignore` and `.dockerignore` — never committed to the repo.

---

## 🧠 Key Concepts Learned

### V1 — Manual AWS Deployment
- Launched EC2, configured security groups, set up ALB
- Debugged CORS errors and unhealthy ALB targets
- Understood the difference between static hosting (S3) and compute (EC2)

### V2 — Docker + Proper Project Structure (current)
- Containerised the Flask app with a multi-stage Dockerfile
- Replaced in-memory storage with a persistent SQLite database
- Used Docker volumes to persist data outside the container
- Restructured project using Flask Blueprints and app factory pattern
- Separated concerns: routes, models, config each have their own place

### Coming Next
- Docker Compose to run Flask + PostgreSQL as a multi-container app
- JWT authentication (register/login endpoints)
- GitHub Actions CI/CD — auto build and deploy on every push to main

---

## 📈 Roadmap

- [x] Deploy Flask app on EC2 manually
- [x] Set up ALB + S3 frontend
- [x] Dockerise the backend
- [x] Add SQLite database with persistent volume
- [x] Restructure with Blueprints and app factory
- [ ] Docker Compose + PostgreSQL
- [ ] JWT Authentication
- [ ] GitHub Actions CI/CD pipeline
- [ ] Redeploy to AWS with Docker

---

## 💰 AWS Cost (V1)

| Service | Cost |
|---|---|
| EC2 t2.micro | $0 (free tier) |
| S3 | ~$0.02 |
| ALB | ~$4 (pro-rated) |
| **Total** | **~$4.50 / week** |

> AWS resources were taken down after V1 to avoid ongoing charges. Will be recreated for final deployment.

---

## 🙏 Resources

- [AWS Zero to Hero — Abhishek Veeramalla](https://youtube.com/@AbhishekVeeramalla)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Built by Kshitij Khule** | [GitHub](https://github.com/kshitij-khule) | [LinkedIn](https://www.linkedin.com/in/kshitijkhule/)