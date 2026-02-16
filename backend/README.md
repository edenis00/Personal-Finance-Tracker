# Personal Finance Tracker API

## Overview
A RESTful API for managing personal finances.

## Features
- User authentication (JWT)
- Income tracking
- Expense tracking
- Savings goals
- Rate limiting
- CORS support

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT

## Installation
```bash
# Clone repository
git clone https://github.com/edenis00/Personal-Finance-Tracker.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
alembic upgrade head

# Run
uvicorn app.main:app --reload
```

## Running with Docker Compose
You can also run the application using Docker Compose from the project root directory.

### Prerequisites
- Docker and Docker Compose installed
- `.env` file configured in the `backend/` directory (see `.env.sample`)

### Start All Services (Backend + Frontend + Database)
```bash
# Navigate to the project root directory
cd Personal-Finance-Tracker

# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### Start Backend Only (with Database)
```bash
# Start only the backend and database services
docker-compose up backend db --build
```

### Stop Services
```bash
# Stop all running containers
docker-compose down

# Stop and remove volumes (will delete database data)
docker-compose down -v
```

### Access the Application
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000 (if running full stack)
- **Database**: localhost:5432

### View Logs
```bash
# View logs for all services
docker-compose logs -f

# View logs for backend only
docker-compose logs -f backend
```

## API Documentation
Visit `/api/v1/docs` for interactive Swagger documentation.

## Environment Variables
See `.env.sample` for required variables.

## Testing
```bash
pytest
```

## License
MIT