# Trailer API

A REST API for managing movie trailers built with FastAPI and SQLAlchemy. The API follows the contract defined in the Roku developers feed structure.

## Setup

### Prerequisites
- Python 3.9+
- `uv` package manager (or pip)

### Installation

1. Install dependencies:
```bash
# Using uv
uv sync

# Or using pip
pip install -r requirements.txt
```

2. Seed the database with trailers from the Roku developers feed:
```bash
# Using uv
uv run python seed.py

# Or directly with Python
python seed.py
```

3. Run the development server:
```bash
# Using uv
uv run uvicorn main:app --reload

# Or directly with uvicorn
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`

## Data Model

The API uses the following trailer structure (from Roku developers feed):

```json
{
  "id": 1,
  "external_id": "shortform-...",
  "title": "BrightScript debug protocol",
  "short_description": "Demonstrates the Roku Remote Debugger",
  "long_description": "This video demonstrates the Roku Remote Debugger...",
  "video_url": "https://image.roku.com/.../roku-brightscript-debug-protocol.mp4",
  "video_path": "/files/roku-brightscript-debug-protocol_video.mp4",
  "thumbnail_url": "https://d6hm6c1vbpfva.cloudfront.net/.../roku-brightscript-network-debug-protocol.jpg",
  "thumbnail_path": "/files/roku-brightscript-debug-protocol_thumbnail.png",
  "release_date": "2020-01-20",
  "duration": 713,
  "genres": "educational",
  "tags": "demo",
  "video_type": "MP4",
  "quality": "HD",
  "language": "en-us",
  "created_at": "2026-10-27T12:00:00",
  "updated_at": "2026-10-27T12:00:00"
}
```

## Endpoints

### Trailers
- `GET /trailers` - List all trailers (with pagination: `?skip=0&limit=10`)
- `GET /trailers/{id}` - Get a specific trailer
- `POST /trailers` - Create a new trailer
- `PUT /trailers/{id}` - Update a trailer
- `DELETE /trailers/{id}` - Delete a trailer

### Static Files
- `GET /files/{filename}` - Access uploaded video and thumbnail files

## Example Usage

### List Trailers
```bash
curl "http://localhost:8000/trailers"
curl "http://localhost:8000/trailers?skip=0&limit=5"
```

### Get a Specific Trailer
```bash
curl "http://localhost:8000/trailers/1"
```

### Create a Trailer
```bash
curl -X POST "http://localhost:8000/trailers" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "my-trailer-1",
    "title": "My Awesome Trailer",
    "short_description": "A brief description",
    "long_description": "A detailed description of the trailer",
    "video_url": "https://example.com/trailer.mp4",
    "video_path": "/files/my-trailer_video.mp4",
    "thumbnail_url": "https://example.com/thumbnail.jpg",
    "thumbnail_path": "/files/my-trailer_thumbnail.png",
    "duration": 120,
    "genres": "action,adventure",
    "tags": "new,featured",
    "video_type": "MP4",
    "quality": "HD",
    "language": "en-us"
  }'
```

### Update a Trailer
```bash
curl -X PUT "http://localhost:8000/trailers/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

### Delete a Trailer
```bash
curl -X DELETE "http://localhost:8000/trailers/1"
```

## Database

The API uses SQLite for storage. The database file (`trailers.db`) is created automatically on first run.

### Seeding

Run `python seed.py` to populate the database with trailers from `seeds/trailers.json`. This script:
- Reads the local `trailers.json` seed file
- Creates trailer records with all metadata
- Avoids duplicate entries based on `external_id`
- References files stored in the `/files` folder (e.g., `http://localhost:8000/files/trailer-name_video.mp4`)

## File Structure

```
trailer-api/
├── main.py              # FastAPI application
├── database.py          # Database setup
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── seed.py              # Database seeding script
├── files/               # Static files (videos, thumbnails)
├── seeds/
│   └── trailers.json    # Seed data with trailer definitions
├── pyproject.toml       # Project config
├── requirements.txt     # Dependencies
└── README.md            # This file
```
