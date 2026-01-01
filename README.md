# EZCTF - Cybersecurity Practice CTF Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/vue-2.x-green.svg)](https://vuejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)

[中文文档](README_zh.md) | [English](README.md)

EZCTF is a modern, decoupled CTF (Capture The Flag) competition platform designed for cybersecurity practice courses. This project adopts the latest FastAPI backend architecture and Vue.js frontend framework, implementing complete functionality from challenge management and dynamic container scheduling to real-time rankings.

## ✨ Features

- **Modern Backend**: Built with **FastAPI** (Python 3.12+), integrating **SQLModel** (SQLAlchemy + Pydantic) and **PostgreSQL**.
- **Responsive Frontend**: Uses **Vue.js** with **Element UI** component library, providing a beautiful and smooth user interaction experience.
- **Core Functions**:
    - **Challenge System**: Supports multiple challenge types such as Web, Pwn, Reverse, Crypto, Misc, etc., with attachment downloads.
    - **Dynamic Environment**: Supports creation and destruction of dynamic container instances (Web/Pwn types).
    - **Judging System**: Dynamic Flag verification and point settlement.
    - **Rankings**: Real-time user and team score leaderboards.
- **User & Team**:
    - Complete user registration, login (JWT authentication), and personal center.
    - Team System: Create team, join/leave team, leader management (kick members, transfer leadership).
- **Engineering Practices**:
    - **Auto Migrations**: Integrated **Alembic**, automatically synchronizing database structure on service startup.
    - **Dependency Management**: Backend uses **uv** for extremely fast package management.
    - **Unit Testing**: Comprehensive Pytest test cases covering core logic.

## 📂 Project Structure

```text
EZCTF/
├── backend/                # FastAPI Backend Project
│   ├── challenges/         # Challenge attachments and Docker env configs
│   ├── src/                # Backend Source Code
│   │   ├── common/         # Common Utilities (Security, Error Handling)
│   │   ├── conf/           # Configuration & Database Connection
│   │   ├── middleware/     # Middleware (JWT Auth)
│   │   ├── task/           # Task Module (CRUD, Judging)
│   │   ├── team/           # Team Module
│   │   ├── user/           # User Module
│   │   ├── main.py         # Application Entry Point
│   │   └── tests/          # Unit Tests
│   ├── pyproject.toml      # Backend Dependencies
│   └── run.sh              # Backend Standalone Startup Script
├── ezctf.top/
│   └── ezctf/              # Vue.js Frontend Project
│       ├── src/
│       │   ├── components/ # Vue Components (Element UI)
│       │   ├── views/      # Page Views
│       │   ├── UserSystemApi/ # Frontend-Backend Interaction API
│       │   └── ...
│       ├── package.json    # Frontend Dependencies
│       └── run.sh          # Frontend Standalone Startup Script
├── run.sh                  # One-click Startup Script
├── stop.sh                 # One-click Stop Script
└── README.md               # Project Documentation
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+** & **uv** (Recommended)
- **Node.js** & **npm**
- **PostgreSQL** (Default config: Database `ezctf`, User/Password `postgres/postgres`)

### One-click Start (Recommended)

Convenient startup and stop scripts are provided in the project root directory:

1.  **Start Services**
    ```bash
    ./run.sh
    ```
    This script automatically checks the environment, installs dependencies, and starts both backend and frontend services.
    - Backend API: `http://localhost:8000`
    - Frontend App: `http://localhost:8080`

2.  **Stop Services**
    ```bash
    ./stop.sh
    ```

### Manual Startup

If you need to debug backend or frontend separately, follow these steps:

#### Backend Startup

1.  **Enter Backend Directory**
    ```bash
    cd backend
    ```

2.  **Start Service**
    ```bash
    chmod +x run.sh
    ./run.sh
    ```
    API Docs: `http://localhost:8000/docs`

#### Frontend Startup

1.  **Enter Frontend Directory**
    ```bash
    cd ezctf.top/ezctf
    ```

2.  **Start Service**
    ```bash
    chmod +x run.sh
    ./run.sh
    ```
    Access: `http://localhost:8080`

## 🛠 Development Guide

### Database Migrations (Backend)

This project uses **Alembic** for database schema migrations.

```bash
cd backend
# Generate migration script (after modifying Models)
uv run alembic revision --autogenerate -m "description"

# Apply migrations manually (automatically executed on service startup)
uv run alembic upgrade head
```

### Running Tests

Run Pytest test suite:

```bash
cd backend
uv run pytest
```

## 📄 Original Requirements

### CTF Website Development
- Support common challenge types like Web, Reverse, Pwn
- Deploy multiple categories of challenges
- Team/Individual Rankings
- Real-name Login

### Report Requirements
- Design Document, Test Document, Presentation Document
- Compilable Code, Demo Video
