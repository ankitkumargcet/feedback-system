# User endpoints
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate
from app.crud import create_user

router = APIRouter()

@router.post("/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)