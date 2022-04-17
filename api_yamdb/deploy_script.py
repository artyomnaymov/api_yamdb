import os
import sqlite3

import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
django.setup()

from reviews.models import Category, Genre, Review, Title, User, Comment


def import_category():
    dataset = pd.read_csv('static/data/category.csv')
    items = []
    for i, row in dataset.iterrows():
        items.append(Category(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        ))
    Category.objects.all().delete()
    Category.objects.bulk_create(items)
    return print('Список категорий успешно импортирован')


def import_genre():
    dataset = pd.read_csv('static/data/genre.csv')
    items = []
    for i, row in dataset.iterrows():
        items.append(Genre(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        ))
    Genre.objects.all().delete()
    Genre.objects.bulk_create(items)
    return print('Список жанров успешно импортирован')


def import_titles():
    dataset = pd.read_csv('static/data/titles.csv')
    items = []
    for i, row in dataset.iterrows():
        items.append(Title(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category'])
        ))
    Title.objects.all().delete()
    Title.objects.bulk_create(items)
    return print('Список произведений успешно импортирован')


def import_genre_titles():
    connections = sqlite3.connect('db.sqlite3')
    sql = 'DELETE FROM reviews_title_genre'
    cur = connections.cursor()
    cur.execute(sql)
    connections.commit()
    import_file = pd.read_csv('static/data/genre_title.csv')
    import_file.to_sql('reviews_title_genre', connections,
                       if_exists='append', index=False)
    connections.close()
    return print('Список жанров фильмов успешно импортирован')


def import_user():
    dataset = pd.read_csv('static/data/users.csv')
    items = []
    for i, row in dataset.iterrows():
        items.append(User(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            password='qwerty123',
        ))
    User.objects.all().delete()
    User.objects.bulk_create(items)
    return print('Список пользователей успешно импортирован')


def import_review():
    dataset = pd.read_csv('static/data/review.csv')
    items = []
    for i, row in dataset.iterrows():
        items.append(Review(
            id=row['id'],
            title=Title.objects.get(id=row['title_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            score=row['score'],
            pub_date=row['pub_date'],
        ))
    Review.objects.all().delete()
    Review.objects.bulk_create(items)
    return print('Список комментариев успешно импортирован')


def import_comment():
    dataset = pd.read_csv('static/data/comments.csv')
    items = []
    for i, row in dataset.iterrows():
        items.append(Comment(
            id=row['id'],
            review=Review.objects.get(id=row['review_id']),
            text=row['text'],
            author=User.objects.get(id=row['author']),
            pub_date=row['pub_date'],
        ))
    Comment.objects.all().delete()
    Comment.objects.bulk_create(items)
    return print('Список комментариев успешно импортирован')


if __name__ == '__main__':
    import_category()
    import_genre()
    import_titles()
    import_genre_titles()
    import_user()
    import_review()
    import_comment()
