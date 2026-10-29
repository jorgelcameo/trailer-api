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

## Authentication

The API uses **JWT Bearer tokens** for authentication. Admin operations (create, update, delete) require authentication.

### Default Admin Credentials
```
username: admin
password: admin123
```

**⚠️ Change these in production via environment variables:**
```bash
export ADMIN_USERNAME=your_admin
export ADMIN_PASSWORD=your_secure_password
export SECRET_KEY=your_secret_key
```

## Endpoints

### Authentication
- `POST /login` - Get JWT access token
- `GET /me` - Get current user info (requires token)

### Trailers (Public Read)
- `GET /trailers` - List all trailers (no auth required)
- `GET /trailers/{id}` - Get specific trailer (no auth required)

### Trailers (Admin Only)
- `POST /trailers` - Create trailer (requires JWT token + admin role)
- `PUT /trailers/{id}` - Update trailer (requires JWT token + admin role)
- `DELETE /trailers/{id}` - Delete trailer (requires JWT token + admin role)

### Static Files
- `GET /files/{filename}` - Access video and thumbnail files

## Example Usage

### 1. Login and Get Token
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. List Trailers (Public - No Auth)
```bash
curl "http://localhost:8000/trailers"
curl "http://localhost:8000/trailers?skip=0&limit=5"
```

### 3. Get Current User Info
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/me"
```

### 4. Create a Trailer (Admin Only)
```bash
TOKEN="your_jwt_token_from_login"

curl -X POST "http://localhost:8000/trailers" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "my-trailer-1",
    "title": "My Awesome Trailer",
    "short_description": "A brief description",
    "long_description": "A detailed description",
    "video_url": "https://api.example.com/files/my-trailer_video.mp4",
    "thumbnail_url": "https://api.example.com/files/my-trailer_thumbnail.png",
    "duration": 120,
    "genres": "action,adventure",
    "tags": "new,featured",
    "video_type": "MP4",
    "quality": "HD",
    "language": "en-us"
  }'
```

### 5. Update a Trailer (Admin Only)
```bash
curl -X PUT "http://localhost:8000/trailers/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

### 6. Delete a Trailer (Admin Only)
```bash
curl -X DELETE "http://localhost:8000/trailers/1" \
  -H "Authorization: Bearer $TOKEN"
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
