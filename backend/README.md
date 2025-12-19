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