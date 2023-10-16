class CreateQuestionError(Exception):
    """Класс ошибки при записи вопроса в базу данных"""

    def __init__(self, exception: Exception):
        self.__exception = exception

    def __str__(self):
        return f'При записи вопроса в базу данных произошла ошибка: {self.__exception}!'
    
    @property
    def exception(self) -> Exception:
        return self.__exception
    

class CommitQuestionError(Exception):
    """Класс ошибки при коммите вопроса в базу данных"""

    def __init__(self, exception: Exception):
        self.__exception = exception

    def __str__(self):
        return f'При коммите вопроса в базу данных произошла ошибка: {self.__exception}!'
