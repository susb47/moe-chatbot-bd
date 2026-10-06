from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from app.database.connection import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)  # To group messages by user/session
    role = Column(String)                    # "user" or "assistant"
    content = Column(Text)
    tier = Column(String, nullable=True)     # "guided_action", "policy_kb", etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # For training feedback later (Thumbs up/down)
    user_rating = Column(Boolean, nullable=True)