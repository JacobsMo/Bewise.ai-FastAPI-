## Процесс сборки проекта:
    1. Скопируйте себе на хост: git clone https://github.com/JacobsMo/Bewise.ai-FastAPI-.git.
    2. Перейдите в корневую папку проекта.
    3. Соберите сервисные образы: docker compose build.
    4. Соберите и запустите контейнеры: docker compose up -d.
    5. Программа готова к работе.

## Пример запроса на localhost:
    URL: http://127.0.0.1:8080/api/quiz/get_questions/
    METHODS: ['POST']
    BODY:
        {
            "questions_count": 5
        }
