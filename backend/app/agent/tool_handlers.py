"""
Implementação real de cada tool declarada em tools.py.
O agent/client.py chama essas funções quando o Claude decide usar uma tool.
"""

from app.rag.retriever import retrieve
from app.db.database import SessionLocal, ProgressEntry


def handle_search_study_material(input_data: dict) -> dict:
    query = input_data.get("query", "")
    domain = input_data.get("domain")
    results = retrieve(query=query, domain=domain, top_k=3)
    return {
        "results": [
            {
                "topic": r["topic"],
                "domain": r["domain"],
                "content": r["content"],
            }
            for r in results
        ]
    }


def handle_generate_quiz(input_data: dict) -> dict:
    """
    Não gera as perguntas aqui (isso é feito pelo próprio Claude no texto
    da resposta, usando o conteúdo retornado por search_study_material).
    Esse handler apenas confirma os parâmetros e devolve contexto relevante
    para o modelo formular boas perguntas.
    """
    topic = input_data.get("topic", "")
    num_questions = input_data.get("num_questions", 3)
    context = retrieve(query=topic, top_k=3)
    return {
        "instruction": (
            f"Gere {num_questions} perguntas de múltipla escolha (4 "
            f"alternativas, 1 correta) sobre '{topic}', baseadas no "
            "conteúdo abaixo. Não revele a resposta correta ainda."
        ),
        "reference_content": [c["content"] for c in context],
    }


def handle_grade_quiz_answer(input_data: dict) -> dict:
    correct = input_data.get("correct_answer", "").strip().lower()
    user_answer = input_data.get("user_answer", "").strip().lower()
    is_correct = correct == user_answer or correct in user_answer
    return {
        "is_correct": is_correct,
        "question": input_data.get("question"),
        "correct_answer": input_data.get("correct_answer"),
        "user_answer": input_data.get("user_answer"),
    }


def handle_save_progress(input_data: dict) -> dict:
    db = SessionLocal()
    try:
        entry = ProgressEntry(
            user_id=input_data.get("user_id", "anon"),
            topic=input_data.get("topic", ""),
            domain=input_data.get("domain"),
            quiz_score=input_data.get("quiz_score"),
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return {"saved": True, "entry_id": entry.id}
    finally:
        db.close()


TOOL_HANDLERS = {
    "search_study_material": handle_search_study_material,
    "generate_quiz": handle_generate_quiz,
    "grade_quiz_answer": handle_grade_quiz_answer,
    "save_progress": handle_save_progress,
}
