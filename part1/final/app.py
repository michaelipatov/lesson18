# В этом финальном задании Вам предстоит написать приложение на Flask
# которое работает с двумя моделями Book и Review.
# 
#
# Для сущности Book должны быть созданы эндпоинты:
# /books        - работает с методами GET, POST
# /books/{id}   - работает с методами GET, PUT, DELETE
#
# Для сущности Review должны быть созданы эндпоинты:
# /reviews      - работает с методами GET, POST
# /reviews/{id} - работает с методами GET, PUT, DELETE
#
# Сведения для заполнения базы данных:
#
# Таблица books:
# +----+-------------------------------+---------------+------+-------+
# | id |              name             |     author    | year | pages |
# +----+-------------------------------+---------------+------+-------+
# | 1  | Гарри Поттер и Тайная Комната | Джоан Роулинг | 1990 |  400  |
# | 2  |       Граф Монте-Кристо       |      Дюма     | 1510 |  1344 |
# | 3  |  Гарри Поттер и Орден Феникса | Джоан Роулинг | 1993 |  500  |
# | 4  |   Гарри Поттер и Кубок Огня   | Джоан Роулинг | 1994 |  600  |
# +----+-------------------------------+---------------+------+-------+
#
# Таблица reviews:
# +----+-------+--------+---------+
# | id |  user | rating | book_id*|
# +----+-------+--------+---------+
# | 1  |  Oleg |   5    |    1    |
# | 2  |  Ivan |   6    |    2    |
# | 3  |  John |   4    |    3    |
# | 4  | Diana |   3    |    4    |
# +----+-------+--------+---------+
# *При создании таблицы reviews присваивать полю book_id свойство Foreign_key
#  необязательно.
#
# Структура вашего приложения должна выглядеть следующим образом:
#
# final
# ├── ./app.py         - Это главный файл, который запускает приложение
# ├── ./config.py      - Здесь мы сохраняем настройки приложения
# ├── ./constants.py   - Здесь мы сохраняем константы
# ├── ./models.py      - Здесь мы сохраняем модели
# ├── ./setup_db.py    - Здесь мы инициализируем базу данных
# ├── ./test.py        - Здесь наши тесты, запустите их, как проверите работу приложения
# └── ./views          
#     ├── ./views/books.py    - view-классы по модели Book
#     └── ./views/reviews.py  - view-классы по модели Review
#
# Пожалуйста, не меняйте название переменной 'app', которая должна 
# содержать экземпляр класса Flask, а также название переменной db,
# в которой вы инициализируете базу данных.
# это необходимо для корректной работы тестов
#
#

from flask import Flask
from flask_restx import Api
from models import Book, Review
from setup_db import db
from views.books import book_ns
from views.reviews import review_ns
from config import Config


def create_app(config):
    app = Flask(__name__)
    #app.url_map.strict_slashes = False
    app.config.from_object(config)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(book_ns)
    api.add_namespace(review_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()
        b1 = Book(id=1, name="Гарри Поттер и Тайная Комната", author="Джоан Роулинг", year=1990, pages=400)
        b2 = Book(id=2, name="Граф Монте-Кристо", author="Александр Дюма", year=1844, pages=1344)
        b3 = Book(id=3, name="Гарри Поттер и Орден Феникса", author="Джоан Роулинг", year=1993, pages=500)
        b4 = Book(id=4, name="Гарри Поттер и Кубок Огня", author="Джоан Роулинг", year=1994, pages=600)

        r1 = Review(id=1, user="Oleg", rating=5, book_id=1)
        r2 = Review(id=2, user="Ivan", rating=6, book_id=2)
        r3 = Review(id=3, user="John", rating=4, book_id=3)
        r4 = Review(id=4, user="Diana", rating=3, book_id=4)

        with db.session.begin():
            db.session.add_all([b1, b2, b3, b4])
            db.session.add_all([r1, r2, r3, r4])


app = create_app(Config())


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
