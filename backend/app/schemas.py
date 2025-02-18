# Pydantic schemas
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

# User Schema
class UserCreate(BaseModel):
    employee_id: str
    full_name: str
    ads_id: str
    manager_id: str
    manager_name: str
    manager_email_hash: str
    department: str
    band: str
    job_title: str
    is_active: bool
    email_hash: str

class UserOut(UserCreate):
    user_id: UUID
    created_at: datetime

# Question Schema
class QuestionCreate(BaseModel):
    question_text: str
    category: str
    question_type: str
    difficulty_level: int

class QuestionOut(QuestionCreate):
    question_id: UUID
    last_used_at: Optional[datetime]

# Response Schema
class ResponseCreate(BaseModel):
    question_id: UUID
    user_id: Optional[UUID]
    response_text: Optional[str] = None
    response_emoji: Optional[int] = None
    response_radio: Optional[str] = None

class ResponseOut(ResponseCreate):
    response_id: UUID
    sentiment: Optional[str]
    submitted_at: datetime