from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.api import chat, progress

app = FastAPI(
    title="AWS CCP Tutor Agent",
    description="Agente de IA para estudar e treinar para a prova AWS Certified Cloud Practitioner.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, restrinja ao domínio do frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(progress.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def health_check():
    return {"status": "ok", "service": "aws-ccp-tutor-agent"}
