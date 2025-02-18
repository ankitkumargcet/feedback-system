# Question endpoints
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_questions_by_type

router = APIRouter()

@router.get("/{question_type}")
def get_questions(question_type: str, db: Session = Depends(get_db)):
    return get_questions_by_type(db, question_type)