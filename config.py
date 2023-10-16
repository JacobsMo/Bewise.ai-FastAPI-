import os
import logging

from dotenv import load_dotenv


load_dotenv('.env-dev')


logging.basicConfig(filename='logs.log', filemode='a')


DEFAULT_HANDLER = logging.StreamHandler()
DEFAULT_HANDLER.setLevel(os.getenv('LOGGING_LEVEL'))
FORMAT = logging.Formatter('[%(asctime)s - %(name)s(%(levelname)s)]: %(message)s')
DEFAULT_HANDLER.setFormatter(FORMAT)


SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = int(os.getenv('SERVER_PORT'))
SERVER_DEBUG = False if str(os.getenv('SERVER_DEBUG')).lower() == 'false' else True


DATABASE_DICT = {
    'host': os.getenv('DATABASE_HOST'),
    'port': int(os.getenv('DATABASE_PORT')),
    'username': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'database': os.getenv('DATABASE_NAME'),
}
