import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.agent.tool_handlers import (
    handle_search_study_material,
    handle_grade_quiz_answer,
    handle_save_progress,
)


def test_handle_search_study_material_returns_results():
    output = handle_search_study_material({"query": "S3 armazenamento"})
    assert "results" in output
    assert len(output["results"]) > 0


def test_handle_grade_quiz_answer_correct():
    output = handle_grade_quiz_answer(
        {
            "question": "Quem é responsável pela segurança DA nuvem?",
            "correct_answer": "AWS",
            "user_answer": "aws",
        }
    )
    assert output["is_correct"] is True


def test_handle_grade_quiz_answer_incorrect():
    output = handle_grade_quiz_answer(
        {
            "question": "Quem é responsável pela segurança DA nuvem?",
            "correct_answer": "AWS",
            "user_answer": "Cliente",
        }
    )
    assert output["is_correct"] is False


def test_handle_save_progress_persists_entry(tmp_path, monkeypatch):
    # usa um banco temporário isolado para não sujar o banco real
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp_path}/test.db"

    import importlib
    from app.db import database as db_module

    importlib.reload(db_module)
    db_module.init_db()

    monkeypatch.setattr(
        "app.agent.tool_handlers.SessionLocal", db_module.SessionLocal
    )

    output = handle_save_progress(
        {"user_id": "test-user", "topic": "IAM", "domain": "Security and Compliance"}
    )
    assert output["saved"] is True
    assert "entry_id" in output
