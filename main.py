from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
from datetime import timedelta

from database import engine, get_db, Base
from models import Trailer as TrailerModel, User as UserModel
from schemas import Trailer, TrailerCreate, TrailerUpdate, Token, User as UserSchema
from security import create_access_token, verify_password, get_password_hash, decode_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ADMIN_USERNAME, ADMIN_PASSWORD

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trailer API", version="0.1.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_admin_user(db: Session):
    existing_admin = db.query(UserModel).filter(UserModel.username == ADMIN_USERNAME).first()
    if not existing_admin:
        admin = UserModel(
            name="Administrator",
            username=ADMIN_USERNAME,
            email="admin@trailers.local",
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            is_admin=True,
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"✓ Admin user created: {ADMIN_USERNAME}")
    else:
        print(f"✓ Admin user already exists: {ADMIN_USERNAME}")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise credentials_exception

    return user


@app.on_event("startup")
def startup():
    db = next(get_db())
    try:
        create_admin_user(db)
    finally:
        db.close()


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to Trailer API", "docs": "/docs"}


@app.post("/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=UserSchema, tags=["auth"])
def get_current_user_info(current_user: UserModel = Depends(get_current_user)):
    return current_user


@app.get("/trailers", response_model=List[Trailer], tags=["trailers"])
def list_trailers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    trailers = db.query(TrailerModel).offset(skip).limit(limit).all()
    return trailers


@app.get("/trailers/{trailer_id}", response_model=Trailer, tags=["trailers"])
def get_trailer(
    trailer_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    trailer = db.query(TrailerModel).filter(TrailerModel.id == trailer_id).first()
    if not trailer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trailer with id {trailer_id} not found",
        )
    return trailer


@app.post("/trailers", response_model=Trailer, status_code=status.HTTP_201_CREATED, tags=["trailers"])
def create_trailer(
    trailer: TrailerCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create trailers",
        )
    db_trailer = TrailerModel(**trailer.model_dump())
    db.add(db_trailer)
    db.commit()
    db.refresh(db_trailer)
    return db_trailer


@app.put("/trailers/{trailer_id}", response_model=Trailer, tags=["trailers"])
def update_trailer(
    trailer_id: int,
    trailer: TrailerUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update trailers",
        )
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
def delete_trailer(
    trailer_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete trailers",
        )
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
