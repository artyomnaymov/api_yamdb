***Проект YaMDb***
---
### Описание:
Проект YaMDb собирает отзывы пользователей на произведения («Книги», «Фильмы», «Музыка»).
Пользователь может оставить развернутый отзыв с выставлением индивидуальной оценки.
У пользователей есть возможность комментировать отзывы

С помощью YaMDb возможно:
* Создавать отзыв на произведение
* Оставить комментарий на  отзыв автора
* Получение/добавление жанров, категорий и наименований произведений

---
### Установка:

1. Создать виртуальное окружение

*python -m venv venv*

2. Активировать виртуальное окружение

*source venv/scripts/activate*

3. Установить зависимости

*pip install -r requirement.txt*

4. Выполнить миграции

*python manage.py makemigrations*

*python manage.py migrate*

5. Запустить проект

*python manage.py runserver*

---
### Доступные методы API запросов:
метод                                            | GET | POST | PUT | PATCH | DEL |
-------------------------------------------------|-----|------|-----|-------|-----|
/api/v1/auth/signup/ | - | V | - | - | - |
/api/v1/auth/token/ | - | V | - | - | - |
/api/v1/categories/  | V | V | - | - | - |
/api/v1/categories/{slug}/  | - | - | - | - | V |
/api/v1/genres/ | V | V | - | - | - |
/api/v1/genres/{slug}/  | - | - | - | - | V |
/api/v1/titles/ | V | V | - | - | - |
/api/v1/titles/{title_id}/ | V | - | - | V | V |
/api/v1/titles/{title_id}/reviews/ | V | V | - | - | - |
/api/v1/titles/{title_id}/reviews/{reviews_id} | V | - | - | V | V |
/api/v1/titles/{title_id}/reviews/comment/ | V | V | - | - | - |
/api/v1/titles/{title_id}/reviews/comment/{comment_id}/ | V | - | - | V | V |
/api/v1/users/ | V | V | - | - | - |
/api/v1/users/{username}/ | V | - | - | V | V |
/api/v1/users/me/ | V | - | - | V | - |

---

### Примеры:
Получение данных о категории

Request:
```
http://127.0.0.1:8000/api/v1/categories/
```
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

---