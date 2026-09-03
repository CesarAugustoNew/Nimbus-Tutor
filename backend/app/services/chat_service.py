"""
Mantém o histórico de conversa por usuário em memória (simples, adequado
para demo/portfólio). Em produção isso viraria uma tabela no banco
(ex: tabela `messages` vinculada a `user_id`/`session_id`).
"""

from app.agent.client import run_agent

_conversations: dict[str, list[dict]] = {}


def send_message(user_id: str, message: str) -> str:
    history = _conversations.get(user_id, [])
    history.append({"role": "user", "content": message})

    result = run_agent(history)
    _conversations[user_id] = result["messages"]

    return result["reply"]


def reset_conversation(user_id: str) -> None:
    _conversations.pop(user_id, None)
