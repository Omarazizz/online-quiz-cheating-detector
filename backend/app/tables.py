from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.sql import func

metadata = MetaData()

submissions = Table(
    "submissions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("student_id", String(50), nullable=False),
    Column("question_id", String(50), nullable=False),
    Column("answer", Text, nullable=False),
    Column("time_taken", Float, nullable=False),
    Column("submitted_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)

cheating_flags = Table(
    "cheating_flags",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("submission_id", Integer, ForeignKey("submissions.id"), nullable=False),
    Column("rule_name", String(100), nullable=False),
    Column("reason", Text, nullable=False),
    Column("score", Integer, nullable=False),
    Column("is_resolved", Boolean, default=False, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)