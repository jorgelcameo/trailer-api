from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base


class Trailer(Base):
    __tablename__ = "trailers"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    short_description = Column(Text)
    long_description = Column(Text)
    video_url = Column(String)
    video_path = Column(String)  # local file path
    thumbnail_url = Column(String)
    thumbnail_path = Column(String)  # local file path
    release_date = Column(DateTime)
    duration = Column(Integer)  # duration in seconds
    genres = Column(String)  # comma-separated genres
    tags = Column(String)  # comma-separated tags
    video_type = Column(String)  # MP4, HLS, DASH, etc.
    quality = Column(String)  # HD, FHD, SD, etc.
    language = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
