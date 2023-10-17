import logging
from typing import NewType, Any, Tuple, Optional

import requests

from config import DEFAULT_HANDLER
from .models import session as session_factory, Question
from .exceptions import RequestAPIError, CommitQuestionError, CreateQuestionError


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(DEFAULT_HANDLER)


_T = NewType('_T', list[Tuple[int, str]])


async def _get_question(id_api: int) -> Optional[Question]:
    session = session_factory()
    question = session.query(Question).filter(Question.id_api == id_api).first()
    return question


async def _request_api(questions_count: int) -> list:
    try:
        response_api = requests.get(f'https://jservice.io/api/random?count={questions_count}')
    except Exception as exception:
        raise RequestAPIError(exception)
    json_questions = response_api.json()
    return json_questions


def _check_unique_question(question_count: int, questions_length: int) -> int:
    difference = question_count - questions_length
    return difference


async def add_question(questions_count: int) -> _T:
    """
    Вложенный try-except потребовался в связи с особенностями sqlalchemy,
    некоторые ошибки возникают только после коммита в базу данных.
    """
    session = session_factory()
    json_questions = await _request_api(questions_count)
    logger.debug(type(json_questions))
    questions = []
    try:
        for json in json_questions:
            try:
                question_on_id = await _get_question(json.get('id'))
                if question_on_id:
                    continue

                question = Question(
                    id_api=json.get('id'),
                    text=json.get('question'),
                    answer=json.get('answer'),
                )
                session.add(question)
                questions.append((int(json.get('id')), str(json.get('question')).replace('&', '').replace('\"', '')))
            except Exception as ex:
                session.rollback()
                logger.error(f'При записе вопроса в базу данных произошла ошибка: {ex}!')
                raise CreateQuestionError(ex)
    
            logger.debug(f'Вопрос с идентификатором {json.get("id")} был успешно записан.')
        session.commit()
    except CreateQuestionError as ex:
        raise CreateQuestionError(ex.exception)
    except Exception as ex:
        session.rollback()
        raise CommitQuestionError(ex)
    
    difference = _check_unique_question(questions_count, len(questions))
    logger.debug(f'difference: {difference}')
    if difference:
        questions += await add_question(difference)

    return questions
