from setup_db import db
from marshmallow import Schema, fields


class Book:
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)
    pages = db.Column(db.Integer)


class Review:
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    book_id = db.Column(db.Integer)


class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    author = fields.Str()
    year = fields.Int()
    pages = fields.Int()


class ReviewSchema(Schema):
    id = fields.Int()
    user = fields.Str()
    rating = fields.Int()
    book_id = fields.Int()
