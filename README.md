# Personal Finance Tracker

![React](https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-JSON_Web_Tokens-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Personal Finance Tracker** is a full-stack web application built with **FastAPI** and **React** that helps users track their income and expenses, manage budgets, and gain insights into their financial health. The application features secure email & JWT authentication, a modular architecture, and Docker-based deployment.

## Features

### 🔐 Authentication
- **Email & Password Registration**: Secure user registration with email verification
- **JWT Authentication**: Secure API access using JSON Web Tokens
- **Password Reset**: Forgot password functionality with email reset links
- **Secure Password Storage**: Passwords are hashed using bcrypt

### 💰 Finance Tracking
- **Income & Expense Tracking**: Log all financial transactions
- **Category Management**: Organize transactions by custom categories
- **Budget Management**: Set monthly budgets for different categories
- **Recurring Transactions**: Automatically create recurring income/expenses

### 📊 Analytics & Reporting
- **Dashboard**: Overview of current financial status
- **Spending Trends**: Visual charts showing spending patterns
- **Budget vs Actual**: Track spending against budget limits
- **Export Data**: Export transaction data to CSV format

### ⚙️ System Features
- **Modular Architecture**: Clean separation of concerns between frontend and backend
- **Dockerized Deployment**: Easy setup with Docker Compose
- **RESTful API**: Well-documented API endpoints
- **Responsive Design**: Mobile-friendly user interface

## Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: [Python 3.10+](https://www.python.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: [python-jose](https://python-jose.readthedocs.io/)
- **Password Hashing**: [bcrypt](https://docs.python.org/3/library/bcrypt.html)
- **Email**: [FastAPI Mail](https://fastapi-mail.readthedocs.io/)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Testing**: [pytest](https://docs.pytest.org/)

### Frontend
- **Framework**: [React 18](https://react.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Charts**: [Recharts](https://recharts.org/)
- **HTTP Client**: [Axios](https://axios-http.com/)
- **Forms**: [React Hook Form](https://react-hook-form.com/)
- **Validation**: [Zod](https://zod.dev/)

### Infrastructure
- **Containerization**: [Docker](https://www.docker.com/)
- **Container Orchestration**: [Docker Compose](https://docs.docker.com/compose/)

## Project Structure

```
Personal-Finance-Tracker/
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core configuration and security
│   │   ├── db/               # Database models and session management
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── services/         # Business logic
│   │   └── main.py           # Application entry point
│   ├── tests/                # Unit and integration tests
│   ├── Dockerfile            # Backend Docker configuration
│   └── docker-compose.yml    # Backend service configuration
│
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service layer
│   │   ├── store/            # State management
│   │   ├── utils/            # Utility functions
│   │   └── App.tsx           # Main application component
│   ├── Dockerfile            # Frontend Docker configuration
│   └── docker-compose.yml    # Frontend service configuration
│
├── docker-compose.yml        # Multi-container Docker setup
├── README.md                 # Project documentation
└── .env.example              # Environment variable template
```

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started) (v24.0+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.20+)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Personal-Finance-Tracker.git
   cd Personal-Finance-Tracker
   ```

2. **Configure environment variables**
   Copy the example environment file and fill in your configuration:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your database credentials and other settings.

3. **Start the application**
   Use Docker Compose to build and start all services:
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:8000](http://localhost:8000)
   - **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Development

To run the application in development mode with hot-reload:

```bash
# Start backend
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# Or start both services
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

## Usage

### User Authentication
1. **Register**: Create a new account with your email and password
2. **Login**: Sign in to access your dashboard
3. **Password Reset**: Use the forgot password feature if needed

### Finance Tracking
1. **Add Transaction**: Click "Add Transaction" on the dashboard
2. **Set Budget**: Configure monthly budgets for different categories
3. **View Reports**: Check the analytics section for insights

## API Documentation

The backend API is documented using Swagger UI. You can access the interactive documentation at:

**[http://localhost:8000/docs](http://localhost:8000/docs)**

## Testing

### Backend Tests
Run the backend tests using pytest:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend pytest
```

### Frontend Tests
Run the frontend tests using npm:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec frontend npm test
```

## Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```env
# Backend Configuration
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_
