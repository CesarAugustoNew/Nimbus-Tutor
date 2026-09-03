import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./study_agent.db")

if not ANTHROPIC_API_KEY:
    print(
        "[aviso] ANTHROPIC_API_KEY não configurada. "
        "Copie .env.example para .env e preencha sua chave."
    )
