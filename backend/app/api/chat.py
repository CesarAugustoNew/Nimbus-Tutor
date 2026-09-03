from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import send_message, reset_conversation

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest):
    reply = send_message(payload.user_id, payload.message)
    return ChatResponse(reply=reply)


@router.post("/reset")
def reset(user_id: str = "anon"):
    reset_conversation(user_id)
    return {"reset": True}
