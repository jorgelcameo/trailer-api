from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from database import engine, get_db, Base
from models import Trailer as TrailerModel
from schemas import Trailer, TrailerCreate, TrailerUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trailer API", version="0.1.0")


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to Trailer API"}


@app.get("/trailers", response_model=List[Trailer], tags=["trailers"])
def list_trailers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    trailers = db.query(TrailerModel).offset(skip).limit(limit).all()
    return trailers


@app.get("/trailers/{trailer_id}", response_model=Trailer, tags=["trailers"])
def get_trailer(trailer_id: int, db: Session = Depends(get_db)):
    trailer = db.query(TrailerModel).filter(TrailerModel.id == trailer_id).first()
    if not trailer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trailer with id {trailer_id} not found",
        )
    return trailer


@app.post("/trailers", response_model=Trailer, status_code=status.HTTP_201_CREATED, tags=["trailers"])
def create_trailer(trailer: TrailerCreate, db: Session = Depends(get_db)):
    db_trailer = TrailerModel(**trailer.model_dump())
    db.add(db_trailer)
    db.commit()
    db.refresh(db_trailer)
    return db_trailer


@app.put("/trailers/{trailer_id}", response_model=Trailer, tags=["trailers"])
def update_trailer(
    trailer_id: int, trailer: TrailerUpdate, db: Session = Depends(get_db)
):
    db_trailer = db.query(TrailerModel).filter(TrailerModel.id == trailer_id).first()
    if not db_trailer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trailer with id {trailer_id} not found",
        )

    update_data = trailer.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_trailer, field, value)

    db.add(db_trailer)
    db.commit()
    db.refresh(db_trailer)
    return db_trailer


@app.delete("/trailers/{trailer_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["trailers"])
def delete_trailer(trailer_id: int, db: Session = Depends(get_db)):
    db_trailer = db.query(TrailerModel).filter(TrailerModel.id == trailer_id).first()
    if not db_trailer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trailer with id {trailer_id} not found",
        )
    db.delete(db_trailer)
    db.commit()
    return None


files_dir = Path(__file__).parent / "files"
files_dir.mkdir(exist_ok=True)

if files_dir.exists():
    app.mount("/files", StaticFiles(directory=str(files_dir)), name="files")
