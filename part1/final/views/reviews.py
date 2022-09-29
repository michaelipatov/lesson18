from flask import request
from flask_restx import Resource, Namespace
from setup_db import db
from models import Review, ReviewSchema


review_ns = Namespace('reviews')
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)


@review_ns.route('/')
class ReviewsView(Resource):
    def get(self):
        return reviews_schema.dump(Review.query.all()), 200

    def post(self):
        data = request.json
        new_review = Review(**data)
        with db.session.begin():
            db.session.add(new_review)
        return "", 201


@review_ns.route('/<int:rid>')
class ReviewView(Resource):
    def get(self, rid: int):
        return review_schema.dump(Review.query.get(rid)), 200


    def put(self, rid: int):
        review = Review.query.get(rid)
        if not review:
            return "", 404
        data = request.json
        review.user = data.get("user")
        review.rating = data.get("rating")
        review.book_id = data.get("book_id")
        db.session.add(review)
        db.session.commit()
        return "", 204


    def delete(self, rid: int):
        review = Review.query.get(rid)
        if not review:
            return "", 404
        db.session.delete(review)
        db.session.commit()
        return "", 204
