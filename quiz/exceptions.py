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
    

class RequestAPIError(Exception):
    """Класс ошибки при запросе к внешнему API"""
    def __init__(self, exception: Exception):
        self.__exception = exception

    def __str__(self):
        return f'При запросе к внешнему API произошла ошибка: {self.__exception}!'
