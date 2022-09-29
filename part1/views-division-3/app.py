# У вас есть приложение с использованием REST X, 
# где все views, а также модель находятся в одном файле. 
# 
# Необходимо сделать рефакторинг архитектуры приложения.
# Структура приложения должна быть следующего вида:
#
# views-division-3
# ├── ./app.py       - Основной фаил, здесь инициализируется приложение
# ├── ./models.py    - В этот фаил переместите модели
# ├── ./setup_db.py  - в этом файле инициализируйте базу данных для Flask
# ├── ./test.py      - Это наши тесты, запустите после самостоятельной проверки
# └── ./views
#     ├── ./views/books.py   - В эти фаилы переместите необходимые
#     └── ./views/authors.py   для работы class based views.
# 
# Требования к выполнению задания:
# - Приложение должно соответствовать структуре выше.
# - В файле app.py не должно быть лишних переменных.
# - Приложение должно запускаться.
# - Запрос на эндпоинт должен возвращать корректный код.
#
# Менять значения, возвращаемые view-функциями, 
# а также url-адреаса в данном задании не требуется.
# Также задание содержит упрощенный вариант сериализации/десериализации
# которым мы пользуемся только в учебных целях для сокращения объема кода.

from flask import Flask
from flask_restx import Api
from models import Book, Author
from setup_db import db
from views.authors import author_ns
from views.books import book_ns


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(book_ns)
    api.add_namespace(author_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()
        a1 = Author(id=1, name="Джоан Роулинг", age=1965)          # Формируем тестовую базу данных
        a2 = Author(id=2, name="Александр Дюма", age=1802)         # для того чтобы можно было
        b1 = Book(id=1, name="Гарри Поттер и Тайная Комната",      # самостоятельно проверить
                author="Джоан Роулинг", year=1990)                 # работу эндпоинтов
        b2 = Book(id=2, name="Граф Монте-Кристо",
                author="Александр Дюма", year=1844)
        b3 = Book(id=3, name="Гарри Поттер и Орден Феникса",
                author="Джоан Роулинг", year=1993)
        with db.session.begin():
            db.session.add_all([b1, b2, b3, a1, a2])


app = create_app()

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
