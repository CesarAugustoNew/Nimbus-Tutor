from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str = "anon"
    message: str


class ChatResponse(BaseModel):
    reply: str
