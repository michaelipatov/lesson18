from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Book, BookSchema


book_ns = Namespace('books')
book_schema = BookSchema()
books_schema = BookSchema(many=True)


@book_ns.route('/')
class BooksView(Resource):
    def get(self):
        return books_schema.dump(Book.query.all()), 200

    def post(self):
        data = request.json
        new_book = Book(**data)
        with db.session.begin():
            db.session.add(new_book)
        return "", 201


@book_ns.route('/<int:bid>')
class BookView(Resource):
    def get(self, bid: int):
        return book_schema.dump(Book.query.get(bid)), 200


    def put(self, bid: int):
        book = Book.query.get(bid)
        if not book:
            return "", 404
        req_json = request.json
        book.name = req_json.get("name")
        book.author = req_json.get("author")
        book.year = req_json.get("year")
        book.pages = req_json.get("pages")

        db.session.add(book)
        db.session.commit()
        return "", 204


    def delete(self, bid: int):
        book = Book.query.get(bid)
        if not book:
            return "", 404
        db.session.delete(book)
        db.session.commit()
        return "", 204
