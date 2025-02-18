# SQLAlchemy models
from sqlalchemy import Column, String, Text, Integer, Boolean, ForeignKey, TIMESTAMP, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

# User Model
class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    ads_id = Column(String, unique=True, nullable=False)
    manager_id = Column(String, nullable=False)
    manager_name = Column(String, nullable=False)
    manager_email_hash = Column(String, nullable=False)
    department = Column(String, nullable=False)
    band = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    email_hash = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

# Question Model
class Question(Base):
    __tablename__ = "questions"
    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_text = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    question_type = Column(String, nullable=False)  # comment, emoji, radio
    difficulty_level = Column(Integer, nullable=False)
    last_used_at = Column(TIMESTAMP, default=None)

# Response Model
class Response(Base):
    __tablename__ = "responses"
    response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    response_text = Column(Text, nullable=True)
    response_emoji = Column(Integer, nullable=True)
    response_radio = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)
    submitted_at = Column(TIMESTAMP, default=func.now())

# ML Question Scores Model
class MLQuestionScore(Base):
    __tablename__ = "ml_question_scores"
    score_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    relevance_score = Column(Float, nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now())