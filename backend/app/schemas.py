from pydantic import BaseModel, Field


class SubmissionCreate(BaseModel):
    student_id: str = Field(min_length=1, max_length=50)
    question_id: str = Field(min_length=1, max_length=50)
    answer: str = Field(min_length=1)
    time_taken: float = Field(gt=0)


class CheatingFlagResponse(BaseModel):
    id: int
    submission_id: int
    rule_name: str
    reason: str
    score: int
    is_resolved: bool