"""
Cliente do agente: encapsula a chamada à Anthropic API e o loop de
tool use (function calling). É aqui que o "agente" de fato decide
usar as ferramentas (buscar conteúdo, gerar quiz, corrigir resposta,
salvar progresso) antes de responder ao usuário.
"""

from anthropic import Anthropic

from app.config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from app.agent.system_prompt import SYSTEM_PROMPT
from app.agent.tools import TOOLS
from app.agent.tool_handlers import TOOL_HANDLERS

client = Anthropic(api_key=ANTHROPIC_API_KEY)

MAX_TOOL_ITERATIONS = 5


def run_agent(messages: list[dict]) -> dict:
    """
    Roda o loop do agente até ele parar de chamar tools e devolver uma
    resposta final em texto.

    `messages` segue o formato da Anthropic API:
    [{"role": "user"/"assistant", "content": ...}, ...]

    Retorna: {"reply": str, "messages": list} — `messages` já inclui o
    histórico atualizado (incluindo os tool calls), pronto para ser
    salvo/reenviado na próxima rodada da conversa.
    """
    conversation = list(messages)

    for _ in range(MAX_TOOL_ITERATIONS):
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=conversation,
        )

        conversation.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            reply_text = "".join(
                block.text for block in response.content if block.type == "text"
            )
            return {"reply": reply_text, "messages": conversation}

        # O modelo quer usar uma ou mais tools: executa e devolve o resultado
        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            handler = TOOL_HANDLERS.get(block.name)
            if handler is None:
                output = {"error": f"tool '{block.name}' não implementada"}
            else:
                output = handler(block.input)

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(output),
                }
            )

        conversation.append({"role": "user", "content": tool_results})

    return {
        "reply": "Desculpa, tive dificuldade para concluir o raciocínio. Pode reformular?",
        "messages": conversation,
    }
