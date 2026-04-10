# Zippy Logitech Backend

FastAPI backend for the Logistics BI Platform.

## Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── models/       # SQLAlchemy models
│   ├── services/     # Business logic
│   └── database/     # Database configuration
├── tests/            # Unit tests
└── requirements.txt  # Python dependencies
```