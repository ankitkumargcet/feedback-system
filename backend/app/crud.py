# DB operations
from sqlalchemy.orm import Session
from app.models import User, Question, Response, MLQuestionScore
from app.schemas import UserCreate, QuestionCreate, ResponseCreate
from sqlalchemy.sql import func

# Create a new user
def create_user(db: Session, user: UserCreate):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Fetch questions based on type
def get_questions_by_type(db: Session, question_type: str):
    return db.query(Question).filter(Question.question_type == question_type).all()

# Submit a response
def submit_response(db: Session, response: ResponseCreate):
    new_response = Response(**response.dict())
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response