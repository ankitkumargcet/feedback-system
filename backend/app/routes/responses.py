# Feedback endpoints
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas import ResponseCreate
from app.crud import submit_response
from pydantic import BaseModel

router = APIRouter()

# Existing endpoint: Add response
@router.post("/")
def add_response(response: ResponseCreate, db: Session = Depends(get_db)):
    return submit_response(db, response)


# ✅ Fixed Endpoint: Update defer/skip state
class StateUpdateRequest(BaseModel):
    question_id: str
    action: str

@router.post("/update_state")
def update_response_state(request: StateUpdateRequest, db: Session = Depends(get_db)):
    if request.action == "defer":
        db.execute(text("""
            UPDATE responses 
            SET defer_count = defer_count + 1 
            WHERE question_id = :qid
        """), {"qid": request.question_id})
    elif request.action == "skip":
        db.execute(text("""
            UPDATE responses 
            SET skipped = TRUE 
            WHERE question_id = :qid
        """), {"qid": request.question_id})
    db.commit()
    return {"status": "success", "action": request.action}