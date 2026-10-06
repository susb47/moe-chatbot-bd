from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from app.core.router import QueryRouter
from app.services.llm_service import GeminiService
from app.database.connection import get_db
from app.database.models import ChatMessage

router = APIRouter()
llm_service = GeminiService()

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default_session" # Frontend will generate a unique ID per user

class ChatResponse(BaseModel):
    response: str
    tier: str
    source: str
    redirect_url: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_handler(payload: ChatRequest, db: Session = Depends(get_db)):
    # 1. Save User Question to DB
    user_msg = ChatMessage(session_id=payload.session_id, role="user", content=payload.query)
    db.add(user_msg)
    db.commit()

    route = QueryRouter.classify_intent(payload.query)
    response_text = ""
    source = ""
    redirect_url = None

    # 2. Route the query
    if route["tier"] == "guided_action":
        response_text = f"দাপ্তরিক কার্যক্রম বা সেবার জন্য সরাসরি পোর্টালে প্রবেশ করুন: {route['action_url']}"
        source = "MoE Directory Registry"
        redirect_url = route["action_url"]
    
    elif route["tier"] == "statistics_lookup":
        response_text = "ব্যানবেইস (BANBEIS) এবং বিবিএস (BBS) এর সর্বশেষ তথ্য অনুযায়ী ডাটাবেজ অনুসন্ধান করা হচ্ছে..."
        source = "BANBEIS Official Tables"

    else:
        # --- THE CONTEXT WINDOW ---
        # Fetch the last 4 messages from this session to give the LLM memory
        past_messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == payload.session_id
        ).order_by(ChatMessage.timestamp.desc()).limit(4).all()
        
        # Format for Gemini
        context_str = "\n".join([f"{msg.role}: {msg.content}" for msg in reversed(past_messages)])
        
        response_text = await llm_service.generate_response(user_query=payload.query, context=context_str)
        source = "Ministry of Education Knowledge Base"

    # 3. Save Assistant Answer to DB
    bot_msg = ChatMessage(
        session_id=payload.session_id, 
        role="assistant", 
        content=response_text, 
        tier=route["tier"]
    )
    db.add(bot_msg)
    db.commit()

    return ChatResponse(
        response=response_text,
        tier=route["tier"],
        source=source,
        redirect_url=redirect_url
    )