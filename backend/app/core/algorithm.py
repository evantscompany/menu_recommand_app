import re
import math
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.models import FeedbackType
from collections import defaultdict, Counter

def get_latest_feedback(db: Session, user_id: int, menu_name: str):
    """
    특정 사용자의 특정 메뉴에 대한 최신 피드백 조회
    """
    return db.query(models.RecommendationFeedback)\
        .filter(models.RecommendationFeedback.user_id == user_id)\
        .filter(models.RecommendationFeedback.menu_name == menu_name)\
        .order_by(models.RecommendationFeedback.created_at.desc())\
        .first()
