## **_Проект YaMDb_**

### Описание

Проект YaMDb собирает отзывы пользователей на произведения («Книги», «Фильмы», «Музыка»).
Пользователь может оставить развернутый отзыв с выставлением индивидуальной оценки.
У пользователей есть возможность комментировать отзывы

С помощью YaMDb возможно:

- Создавать отзыв на произведение
- Оставить комментарий на отзыв автора
- Получение/добавление жанров, категорий и наименований произведений

### Стек технологий

- проект написан на Python с использованием Django REST Framework
- библиотека Simple JWT - работа с JWT-токеном

---

### Установка

1. Создать виртуальное окружение

`python -m venv venv`

2. Активировать виртуальное окружение

`source venv/scripts/activate`

3. Установить зависимости

`pip install -r requirement.txt`

4. Выполнить миграцию БД

`python manage.py migrate`

5. Выполнить миграцию данных

`deploy_script.py`

6. Запустить проект

`python manage.py runserver`

---

### Доступные методы API

| Метод                                                   | GET | POST | PUT | PATCH | DEL |
|---------------------------------------------------------|-----|------|-----|-------|-----|
| /api/v1/auth/signup/                                    | -   | V    | -   | -     | -   |
| /api/v1/auth/token/                                     | -   | V    | -   | -     | -   |
| /api/v1/categories/                                     | V   | V    | -   | -     | -   |
| /api/v1/categories/{slug}/                              | -   | -    | -   | -     | V   |
| /api/v1/genres/                                         | V   | V    | -   | -     | -   |
| /api/v1/genres/{slug}/                                  | -   | -    | -   | -     | V   |
| /api/v1/titles/                                         | V   | V    | -   | -     | -   |
| /api/v1/titles/{title_id}/                              | V   | -    | -   | V     | V   |
| /api/v1/titles/{title_id}/reviews/                      | V   | V    | -   | -     | -   |
| /api/v1/titles/{title_id}/reviews/{reviews_id}          | V   | -    | -   | V     | V   |
| /api/v1/titles/{title_id}/reviews/comment/              | V   | V    | -   | -     | -   |
| /api/v1/titles/{title_id}/reviews/comment/{comment_id}/ | V   | -    | -   | V     | V   |
| /api/v1/users/                                          | V   | V    | -   | -     | -   |
| /api/v1/users/{username}/                               | V   | -    | -   | V     | V   |
| /api/v1/users/me/                                       | V   | -    | -   | V     | -   |

---

### Примеры запросов

Получение данных о категории

Request:
`/api/v1/categories/`

Response:

```
[
{
"count": 0,
"next": "string",
"previous": "string",
"results": []
}
]
```
