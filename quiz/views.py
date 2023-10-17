import logging
from typing import Any

import requests
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from config import DEFAULT_HANDLER
from .schemas import QuestionsCount, QuestionsOutput
from .models import session as session_factory, Question
from .exceptions import CreateQuestionError, CommitQuestionError
from .services import add_question


quiz_router = APIRouter(
    prefix='/quiz',
    tags=['Quiz'],
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(DEFAULT_HANDLER)


@quiz_router.post('/get', response_model=QuestionsOutput)
async def get_questions(questions_count: QuestionsCount) -> Response:
    questions = await add_question(questions_count.questions_count)
    response = QuestionsOutput(**{'questions': [dict([('id', question[0]), ('question', question[1])]) for question in questions]})
    return JSONResponse(content=response.dict(), status_code=status.HTTP_201_CREATED)
