from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class TrailerBase(BaseModel):
    title: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    video_url: Optional[str] = None
    video_path: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail_path: Optional[str] = None
    release_date: Optional[datetime] = None
    duration: Optional[int] = None
    genres: Optional[str] = None
    tags: Optional[str] = None
    video_type: Optional[str] = None
    quality: Optional[str] = None
    language: Optional[str] = None


class TrailerCreate(TrailerBase):
    external_id: str


class TrailerUpdate(BaseModel):
    title: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    video_url: Optional[str] = None
    video_path: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail_path: Optional[str] = None
    release_date: Optional[datetime] = None
    duration: Optional[int] = None
    genres: Optional[str] = None
    tags: Optional[str] = None
    video_type: Optional[str] = None
    quality: Optional[str] = None
    language: Optional[str] = None


class Trailer(TrailerBase):
    id: int
    external_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
