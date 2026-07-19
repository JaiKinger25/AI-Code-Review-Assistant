# AI Code Review Assistant 🚀

## Overview

AI Code Review Assistant is a full-stack web application that performs automated code reviews for Python files. It analyzes uploaded code using Pylint, Bandit, and Radon, then generates AI-powered suggestions to improve code quality, security, and maintainability.

---

## Features

- 🔐 User Authentication (JWT)
- 📂 Upload Python (.py) Files
- ✅ Pylint Code Quality Analysis
- 🔒 Bandit Security Analysis
- 📊 Radon Complexity Analysis
- 🤖 AI-Powered Code Review
- 📋 Copy AI Review
- 📥 Download AI Review
- 📂 Upload History
- 🔍 Search Upload History
- 🎨 Responsive Dashboard

---

## Tech Stack

### Frontend
- React.js
- Vite
- Axios
- CSS

### Backend
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt

### Static Analysis Tools
- Pylint
- Bandit
- Radon

---

## Project Structure

```text
AI-Code-Review-Assistant
│
├── backend
│   ├── models
│   ├── routes
│   ├── uploads
│   ├── reports
│   ├── app.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## Installation

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Application Workflow

1. Register or Login
2. Upload a Python (.py) file
3. Run static analysis
4. Generate AI review
5. Display reports
6. Copy or download AI review

---

## Analysis Performed

- Pylint (Code Quality)
- Bandit (Security Analysis)
- Radon (Complexity Analysis)
- AI Review Engine

---

## Future Enhancements

- GitHub Repository Review
- PDF Report Export
- Multi-language Support
- Docker Deployment
- Dark Mode
- Team Collaboration

---

## Developer

**Aditi Jadhav**

Diploma Student

Internship Project

July 2026