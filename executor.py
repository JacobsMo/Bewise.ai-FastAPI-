import logging

import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from config import DEFAULT_HANDLER, SERVER_HOST, SERVER_PORT, SERVER_DEBUG
from quiz.views import quiz_router
from quiz.exceptions import CommitQuestionError, CreateQuestionError, RequestAPIError


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(DEFAULT_HANDLER)


fastapi_application = FastAPI(version='1.0.0', debug=SERVER_DEBUG, title='TestCase')
fastapi_application.include_router(quiz_router)


response_error_500_http = JSONResponse(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content={
        'type': 'Error',
        'exception': 'Внутренняя ошибка сервера!',
    }
)


@fastapi_application.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exception: ValidationError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            'type': 'Error',
            'exception': exception.json(),
        }
    )


@fastapi_application.exception_handler(CommitQuestionError)
async def commit_question_error_handler(request: Request, exception: CommitQuestionError) -> Response:
    return response_error_500_http


@fastapi_application.exception_handler(CreateQuestionError)
async def create_question_error_handler(request: Request, exception: CreateQuestionError) -> Response:
    return response_error_500_http


@fastapi_application.exception_handler(RequestAPIError)
async def request_api_error(reqest: Request, exception: RequestAPIError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'type': 'Error',
            'message': exception,
            'details': exception.exception
        }
    )


if __name__ == '__main__':
    logger.debug('Server is start')
    uvicorn.run(app='executor:fastapi_application', host=SERVER_HOST, port=SERVER_PORT, reload=SERVER_DEBUG)
