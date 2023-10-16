from sqlalchemy.orm import declarative_base


base = declarative_base()


# Инициализировать модель:
from quiz.models import Question
