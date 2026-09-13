from datetime import timedelta

from sqlalchemy import select

from app.tables import submissions


ANSWER_KEY = {
    "Q001": "A",
    "Q002": "C",
    "Q003": "B",
    "Q004": "D",
    "Q005": "A",
}


def detect_cheating(connection, submission):
    flags = []

    # Rule 1: answer submitted unrealistically fast
    if submission["time_taken"] < 2:
        flags.append(
            {
                "rule_name": "too_fast",
                "reason": "Answer was submitted in under 2 seconds.",
                "score": 40,
            }
        )

    # Rule 2: compare current speed with the student's
    # rolling average from their last 5 submissions
    previous_times = connection.execute(
        select(submissions.c.time_taken)
        .where(
            submissions.c.student_id == submission["student_id"],
            submissions.c.id != submission["id"],
        )
        .order_by(submissions.c.submitted_at.desc())
        .limit(5)
    ).scalars().all()

    if previous_times:
        rolling_average = sum(previous_times) / len(previous_times)

        if submission["time_taken"] < rolling_average * 0.5:
            flags.append(
                {
                    "rule_name": "faster_than_usual",
                    "reason": (
                        "Student answered much faster than "
                        "their recent rolling average."
                    ),
                    "score": 30,
                }
            )

    # Rule 3: same wrong answer as another student within 5 seconds
    correct_answer = ANSWER_KEY.get(submission["question_id"])

    if correct_answer is not None and submission["answer"] != correct_answer:
        window_start = submission["submitted_at"] - timedelta(seconds=5)

        matching_submission = connection.execute(
            select(submissions.c.id).where(
                submissions.c.question_id == submission["question_id"],
                submissions.c.answer == submission["answer"],
                submissions.c.student_id != submission["student_id"],
                submissions.c.submitted_at >= window_start,
                submissions.c.submitted_at <= submission["submitted_at"],
                submissions.c.id != submission["id"],
            )
        ).first()

        if matching_submission:
            flags.append(
                {
                    "rule_name": "same_wrong_answer",
                    "reason": (
                        "Another student submitted the same wrong "
                        "answer within 5 seconds."
                    ),
                    "score": 35,
                }
            )

    risk_score = min(
        sum(flag["score"] for flag in flags),
        100,
    )

    return {
        "flags": flags,
        "risk_score": risk_score,
    }