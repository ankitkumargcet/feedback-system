# ML sentiment analysis
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sqlalchemy.orm import Session
from app.models import Response, Question
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# Function to analyze sentiment of a user's feedback
def analyze_sentiment(text):
    score = sia.polarity_scores(text)
    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function to get relevant questions based on user feedback
def get_ml_selected_questions(db: Session, user_id):
    # Fetch user responses
    responses = db.query(Response).filter(Response.user_id == user_id).all()
    if not responses:
        return db.query(Question).order_by(Question.difficulty).limit(5).all()

    # Extract feedback text
    feedback_texts = [resp.response for resp in responses]
    
    # Perform sentiment analysis
    sentiments = [analyze_sentiment(text) for text in feedback_texts]
    
    # Fetch all questions
    all_questions = db.query(Question).all()
    question_texts = [q.question_text for q in all_questions]

    # Apply TF-IDF to measure question similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(feedback_texts + question_texts)
    feedback_vectors = vectors[: len(feedback_texts)]
    question_vectors = vectors[len(feedback_texts) :]

    # Compute relevance scores (dummy approach for now)
    scores = question_vectors.sum(axis=0).A1
    ranked_questions = sorted(zip(all_questions, scores), key=lambda x: x[1], reverse=True)

    # Select top 5 relevant questions
    return [q[0] for q in ranked_questions[:5]]