from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TrailerBase(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    release_date: Optional[datetime] = None
    duration: Optional[int] = None


class TrailerCreate(TrailerBase):
    pass


class TrailerUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    release_date: Optional[datetime] = None
    duration: Optional[int] = None


class Trailer(TrailerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
