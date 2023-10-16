import logging
from typing import Any

import requests
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse

from config import DEFAULT_HANDLER
from .schemas import QuestionsCount, QuestionsOutput
from .models import session as session_factory, Question
from .exceptions import CreateQuestionError, CommitQuestionError


quiz_router = APIRouter(
    prefix='/quiz',
    tags=['Quiz'],
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(DEFAULT_HANDLER)


@quiz_router.post('/get', response_model=QuestionsOutput)
async def get_questions(questions_count: QuestionsCount) -> Response:
    """
    Вложенный try-except потребовался в связи с особенностями sqlalchemy,
    некоторые ошибки возникают только после коммита в базу данных.
    """
    response_api = requests.get(f'https://jservice.io/api/random?count={questions_count.questions_count}')
    json_questions = response_api.json()
    session = session_factory()
    questions = []
    try:
        for json in json_questions:
            try:
                question = Question(
                    id_api=json.get('id'),
                    text=json.get('question'),
                    answer=json.get('answer'),
                )
                session.add(question)
                questions.append((int(json.get('id')), str(json.get('question')).strip('\\')))
            except Exception as ex:
                session.rollback()
                logger.error(f'При записи вопроса в базу данных произошла ошибка: {ex}!')
                raise CreateQuestionError(ex)
    
            logger.debug(f'Вопрос с идентификатором {json.get("id")} был успешно записан.')
        session.commit()
    except CreateQuestionError as ex:
        raise CreateQuestionError(ex.exception)
    except Exception as ex:
        session.rollback()
        raise CommitQuestionError(ex)
    response = QuestionsOutput(**{'questions': [dict([('id', question[0]), ('question', question[1])]) for question in questions]})
    return JSONResponse(content=response.dict(), status_code=status.HTTP_201_CREATED)
