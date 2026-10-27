from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base


class Trailer(Base):
    __tablename__ = "trailers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    video_url = Column(String)
    thumbnail_url = Column(String)
    release_date = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer)  # duration in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
