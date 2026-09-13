from fastapi import APIRouter
from sqlalchemy import select

from app.database import engine
from app.schemas import SubmissionCreate
from app.services.cheating_detector import detect_cheating
from app.services.connection_manager import manager
from app.tables import cheating_flags, submissions

router = APIRouter(prefix="/api/submissions", tags=["submissions"])


@router.post("")
async def create_submission(payload: SubmissionCreate):
    with engine.begin() as connection:
        submission_result = connection.execute(
            submissions.insert()
            .values(
                student_id=payload.student_id,
                question_id=payload.question_id,
                answer=payload.answer,
                time_taken=payload.time_taken,
            )
            .returning(
                submissions.c.id,
                submissions.c.student_id,
                submissions.c.question_id,
                submissions.c.answer,
                submissions.c.time_taken,
                submissions.c.submitted_at,
            )
        )

        submission = dict(submission_result.mappings().one())

        detection = detect_cheating(connection, submission)

        saved_flags = []

        for flag in detection["flags"]:
            flag_result = connection.execute(
                cheating_flags.insert()
                .values(
                    submission_id=submission["id"],
                    rule_name=flag["rule_name"],
                    reason=flag["reason"],
                    score=flag["score"],
                )
                .returning(
                    cheating_flags.c.id,
                    cheating_flags.c.submission_id,
                    cheating_flags.c.rule_name,
                    cheating_flags.c.reason,
                    cheating_flags.c.score,
                    cheating_flags.c.is_resolved,
                    cheating_flags.c.created_at,
                )
            )

            saved_flags.append(dict(flag_result.mappings().one()))

    event = {
        "type": "new_submission",
        "submission": submission,
        "flags": saved_flags,
        "risk_score": detection["risk_score"],
    }

    await manager.broadcast(event)

    return event


@router.get("/recent")
def get_recent_submissions():
    with engine.connect() as connection:
        rows = connection.execute(
            select(submissions)
            .order_by(submissions.c.submitted_at.desc())
            .limit(20)
        ).mappings().all()

        results = []

        for row in rows:
            submission = dict(row)

            flag_rows = connection.execute(
                select(cheating_flags).where(
                    cheating_flags.c.submission_id == submission["id"]
                )
            ).mappings().all()

            flags = [dict(flag) for flag in flag_rows]

            risk_score = min(
                sum(flag["score"] for flag in flags),
                100,
            )

            results.append(
                {
                    "type": "history",
                    "submission": submission,
                    "flags": flags,
                    "risk_score": risk_score,
                }
            )

    return results