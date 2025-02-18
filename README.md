# feedback_system
This repository will be used to host documentation required for feedback system

## Setting up Postgres database
`cd feedback-system/database`

# Start PostgreSQL container
`docker-compose up -d`

# Check PostgreSQL container logs
`docker logs pulsebot-db`

## Run Backend
`cd feedback-system/backend`
`uvicorn app.main:app --reload`
`python3 popup/popup.py`