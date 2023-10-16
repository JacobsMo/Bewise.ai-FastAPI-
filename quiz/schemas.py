from pydantic import BaseModel, Field


class QuestionsCount(BaseModel):
    questions_count: int = Field(ge=1, le=256)


class Question(BaseModel):
    id: int = Field(ge=0)
    question: str


class QuestionsOutput(BaseModel):
    questions: list[Question]
