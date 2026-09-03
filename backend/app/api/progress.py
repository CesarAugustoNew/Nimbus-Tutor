from fastapi import APIRouter

from app.db.database import SessionLocal, ProgressEntry

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/{user_id}")
def get_progress(user_id: str):
    db = SessionLocal()
    try:
        entries = (
            db.query(ProgressEntry)
            .filter(ProgressEntry.user_id == user_id)
            .order_by(ProgressEntry.created_at.desc())
            .all()
        )
        return [
            {
                "topic": e.topic,
                "domain": e.domain,
                "quiz_score": e.quiz_score,
                "created_at": e.created_at.isoformat(),
            }
            for e in entries
        ]
    finally:
        db.close()
