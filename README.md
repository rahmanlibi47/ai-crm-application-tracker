# CareerLedger - AI-Powered Job Application Tracker

A production-style microservices project built to demonstrate modern backend, cloud, and AI engineering concepts.

## Overview

The AI-Powered Job Application Tracker helps users manage job applications, analyze resumes, receive AI-powered feedback, track interview progress, and automate notifications.

This project is being built using a microservices architecture with FastAPI, PostgreSQL, Redis, RabbitMQ, Docker, Kubernetes, AWS, and AI technologies.

---

## Architecture

```text
Frontend
    ↓
API Gateway

├── Auth Service
├── Application Service
├── AI Service
└── Notification Service

Infrastructure:
- PostgreSQL
- Redis
- RabbitMQ
- Docker
- Kubernetes
- AWS
- Prometheus
- Grafana
```

---

## Services

### Auth Service

Current Status: In Progress

Features:

* User Registration
* User Login
* Password Hashing (bcrypt)
* JWT Authentication
* Protected Routes
* PostgreSQL Integration
* Unit Tests

Endpoints:

* GET /health
* POST /signup
* POST /login
* GET /get_user
* GET /oauth/google/login
* GET /oauth/google/callback

### Application Service

Planned Features:

* Company Management
* Job Application Tracking
* Application Status History
* Dashboard Metrics

### AI Service

Planned Features:

* Resume Upload
* Resume Analysis
* Job Match Scoring
* RAG-based Career Assistant
* Embedding Storage

### Notification Service

Planned Features:

* Email Notifications
* Interview Reminders
* SendGrid Integration
* Celery Workers
* RabbitMQ Events

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

### Authentication

* JWT
* OAuth
* bcrypt

### Messaging

* RabbitMQ
* AWS SQS

### Caching

* Redis

### Background Processing

* Celery
* AWS Lambda

### Infrastructure

* Docker
* Kubernetes
* AWS RDS

### Monitoring

* Prometheus
* Grafana

### Frontend

* React
* TypeScript

---

## Current Progress

### Completed

* Auth Service Setup
* PostgreSQL Integration
* User Model
* Signup Endpoint
* Login Endpoint
* JWT Token Generation
* Google OAuth Login
* Protected Route (/get_user)
* Basic Unit Tests

### Next Steps

* Refresh Tokens
* Email Verification
* Application Service
* Docker Compose
* Redis Integration
* RabbitMQ Integration

---

## Running Auth Service

```bash
uvicorn app.main:app --reload --port 8001
```

Swagger UI:

```text
http://localhost:8001/docs
```

---

## Author

Libin Rahman
