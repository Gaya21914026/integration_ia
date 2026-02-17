from fastapi import APIRouter, Depends
from app.schemas.chat import ChatResponse,ChatRequest
from app.dependencies.auth import get_current_user
from app.services.chat import openrouter_chat

router = APIRouter(prefix="/chat",
                   tags=["CHAT WITH IA"],
                   dependencies=[Depends(get_current_user)]
                   )

@router.post("", response_model=ChatResponse)
async def chat_with_ai(data: ChatRequest): 
    ai_message = await openrouter_chat(data.message, data.role) 
    return ChatResponse(response=ai_message )