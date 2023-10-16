import uuid
from datetime import datetime

from sqlalchemy import create_engine, URL, Column, Text, DateTime, \
                        PrimaryKeyConstraint, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID

from config import DATABASE_DICT
from database import base


url = URL.create(
    drivername='postgresql',
    **DATABASE_DICT
)
engine = create_engine(url, echo=False)


class Question(base):
    __tablename__ = 'questions'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True, name='question_id')
    text = Column(Text(), nullable=False, name='question_text')
    answer = Column(Text(), nullable=False, name='question_answer')
    created_at = Column(DateTime(), nullable=False, default=datetime.now)

    __table_args__ = (
        PrimaryKeyConstraint('question_id', name='questions_question_id_pk'),
        UniqueConstraint('question_text'),
        Index('questions_text_idx', 'question_text'),
    )
