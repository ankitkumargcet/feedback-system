# Entry point
from fastapi import FastAPI
from app.database import engine, Base
from app.routes import users, questions, responses

# Initialize DB schema
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PulseBot API")

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(responses.router, prefix="/responses", tags=["Responses"])

@app.get("/")
def health_check():
    return {"message": "PulseBot API is running!"}