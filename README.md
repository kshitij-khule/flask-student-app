# 🎓 Student Management API

A production-ready REST API with JWT authentication, containerized deployment, and automated CI/CD — built to learn real-world backend and DevOps practices.

[![Flask](https://img.shields.io/badge/Flask-3.1-blue?logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://www.postgresql.org/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions)](https://github.com/features/actions)

---

## 🎯 About

This project demonstrates production-grade backend development practices: authentication, database design, containerization, and automated deployment pipelines. Built as a learning project to understand how modern cloud applications are architected and deployed.

**Focus areas:** DevOps practices, security (password hashing, JWT), Docker, CI/CD automation, cloud deployment.

---

## 🏗️ Architecture

```
Client
  ↓
Flask API (Docker container)
  ↓
PostgreSQL (Docker container)
  ↓
Docker Compose orchestrates both
  ↓
GitHub Actions CI/CD pipeline (automated testing & deployment)
```

**Tech Stack:**
- **Backend:** Python 3.11, Flask, Gunicorn (WSGI server)
- **Database:** PostgreSQL 15
- **Authentication:** JWT (JSON Web Tokens), bcrypt password hashing
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud:** AWS (EC2, ALB, S3) — deployment in progress

---

## 🔌 API Endpoints

### Public Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/auth/register` | Create new user account |
| POST | `/auth/login` | Login and receive JWT token |

### Protected Endpoints (Requires JWT Token)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/students/` | Get all students |
| POST | `/students/` | Add a new student |

**Authentication:**
Protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

---

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### Run with Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/kshitij-khule/flask-student-app.git
cd flask-student-app

# Create .env file with required variables
cp .env.example .env

# Start both Flask and PostgreSQL containers
docker compose up

# The API will be available at http://localhost:5000
```

### Test the API

```bash
# 1. Register a new user
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# 2. Login and get JWT token
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# Copy the token from the response, then:

# 3. Add a student (replace YOUR_TOKEN with actual token)
curl -X POST http://localhost:5000/students/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name": "John Doe", "age": 20}'

# 4. Get all students
curl http://localhost:5000/students/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📁 Project Structure

```
flask-student-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # App factory pattern
│   │   ├── config.py            # Environment-based configuration
│   │   ├── routes/
│   │   │   ├── students.py      # Student CRUD endpoints
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   └── health.py        # Health check endpoint
│   │   └── models/
│   │       └── user.py          # User database operations
│   ├── run.py                   # Application entry point
│   ├── test_app.py              # Pytest test suite
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Multi-stage Docker build
│   └── .dockerignore
├── docker-compose.yml           # Multi-container orchestration
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD pipeline
├── .env.example                 # Environment variables template
├── .gitignore
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://admin:password@postgres:5432/studentsdb
POSTGRES_DB=studentsdb
POSTGRES_USER=admin
POSTGRES_PASSWORD=password

# Flask
SECRET_KEY=your-secret-key-here

# CORS
ALLOWED_ORIGINS=http://localhost:5500
```

> **Security Note:** `.env` is in `.gitignore` and never committed. Use `.env.example` as a template.

---

## 🔒 Authentication Flow

1. **Register:** User creates account → password is hashed with bcrypt → stored in PostgreSQL
2. **Login:** User submits credentials → password hash is verified → JWT token generated and returned
3. **Protected Routes:** User includes token in Authorization header → `@token_required` decorator verifies signature and expiry → route executes if valid

**Security Features:**
- Passwords hashed with bcrypt (never stored in plain text)
- JWT tokens signed with HS256 algorithm
- Tokens expire after 24 hours
- Signature verification prevents token tampering

---

## 🐳 Docker Implementation

**Multi-stage Dockerfile:**
- Stage 1 (Builder): Installs dependencies in isolation
- Stage 2 (Runtime): Copies only necessary files, runs as non-root user

**Docker Compose:**
- Flask container depends on PostgreSQL health check
- Volumes persist database data across container restarts
- Internal network allows containers to communicate by service name

---

## 🔄 CI/CD Pipeline

**GitHub Actions Workflow** (`.github/workflows/ci.yml`):

On every push to `main`:
1. Checkout code
2. Install dependencies
3. Run pytest test suite
4. Build Docker image
5. Push to GitHub Container Registry (ghcr.io)

Tests must pass before image is built and pushed.

---

## 🧠 Technical Decisions & Learnings

### Why Docker?
Ensures consistent environments across development, testing, and production. "Works on my machine" is solved by shipping the entire environment.

### Why PostgreSQL over SQLite?
- Production-ready (handles concurrent connections)
- ACID compliance
- Better for cloud deployment (can be separated as managed service)

### Why JWT over Sessions?
- Stateless authentication (no server-side session storage)
- Scalable across multiple servers
- Easy to use with SPAs and mobile apps

### Key Challenges Solved
- **Gunicorn race condition:** Two workers trying to create DB tables simultaneously → fixed with PostgreSQL advisory locks
- **Docker volume permissions:** Container couldn't write to mounted folder → fixed with proper permissions
- **CI/CD test failures:** Environment dependencies not set correctly → fixed with TESTING environment variable

---

## 📈 Roadmap

- [x] Basic Flask API with in-memory storage
- [x] Dockerize the application
- [x] PostgreSQL database with Docker Compose
- [x] JWT authentication (register/login)
- [x] Password hashing with bcrypt
- [x] GitHub Actions CI/CD pipeline
- [x] Automated testing with pytest
- [ ] Deploy to AWS (EC2, ALB, RDS)
- [ ] Add Update and Delete student endpoints
- [ ] Frontend implementation
- [ ] Rate limiting
- [ ] Logging and monitoring

---

## 🙏 Acknowledgments

- [AWS Zero to Hero — Abhishek Veeramalla](https://youtube.com/@AbhishekVeeramalla)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Built by Kshitij Khule** | [GitHub](https://github.com/kshitij-khule) | [LinkedIn](https://www.linkedin.com/in/kshitijkhule/)

---

*This project was built to learn production DevOps and backend practices. While the student management domain is simple, the focus is on infrastructure, security, containerization, and deployment automation.*