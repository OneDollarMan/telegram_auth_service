Запуск:
1. Переименовать example.env в .env
2. Добавить в .env название и токен бота
3. Запустить контейнеры:```docker compose up```
4. Применить миграции ```docker exec -it django python manage.py migrate```

Страница авторизации: http://127.0.0.1:8000/
