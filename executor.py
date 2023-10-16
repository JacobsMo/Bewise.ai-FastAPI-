import logging

import uvicorn
from fastapi import FastAPI

from config import DEFAULT_HANDLER, SERVER_HOST, SERVER_PORT, SERVER_DEBUG
from quiz.views import quiz_router


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(DEFAULT_HANDLER)


fastapi_application = FastAPI(version='1.0.0', debug=SERVER_DEBUG, title='TestCase')
fastapi_application.include_router(quiz_router)


if __name__ == '__main__':
    logger.debug('Server is start')
    uvicorn.run(app='executor:fastapi_application', host=SERVER_HOST, port=SERVER_PORT, reload=SERVER_DEBUG)
