# Trailer API

A REST API for managing movie trailers built with FastAPI and SQLAlchemy.

## Setup

### Prerequisites
- Python 3.9+
- `uv` package manager

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Run the development server:
```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`

## Endpoints

### Trailers
- `GET /trailers` - List all trailers (with pagination)
- `GET /trailers/{id}` - Get a specific trailer
- `POST /trailers` - Create a new trailer
- `PUT /trailers/{id}` - Update a trailer
- `DELETE /trailers/{id}` - Delete a trailer

## Example Usage

### Create a Trailer
```bash
curl -X POST "http://localhost:8000/trailers" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inception",
    "description": "A mind-bending thriller",
    "video_url": "https://example.com/inception.mp4",
    "thumbnail_url": "https://example.com/inception.jpg",
    "duration": 148
  }'
```

### List Trailers
```bash
curl "http://localhost:8000/trailers"
```

### Get a Specific Trailer
```bash
curl "http://localhost:8000/trailers/1"
```

### Update a Trailer
```bash
curl -X PUT "http://localhost:8000/trailers/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Inception (Updated)"}'
```

### Delete a Trailer
```bash
curl -X DELETE "http://localhost:8000/trailers/1"
```

## Database

The API uses SQLite for storage. The database file (`trailers.db`) is created automatically on first run.
