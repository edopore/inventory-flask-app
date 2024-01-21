from flask import Flask
from flask_restful import Api, Resource, abort, marshal_with
from uuid import uuid4

from serializer import book_put_args, resource_fields, checkBook

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdatabase.db"

from model import db, BookModel


class Books(Resource):
    @marshal_with(resource_fields)
    def get(self):
        books = BookModel.query.all()
        return books, 200


class Book(Resource):
    @marshal_with(resource_fields)
    def get(self,book_id):
        book = BookModel.query.get(book_id)
        checkBook(book)
        return book, 200
    
    def delete(self,book_id):
        book = BookModel.query.get(book_id)
        checkBook(book)
        db.session.delete(book)
        db.session.commit()
        return {"message":"book has been deleted","code":204}
    
    @marshal_with(resource_fields)
    def patch(self,book_id):
        args = book_put_args.parse_args()
        book = BookModel.query.get(book_id)
        checkBook(book)
        if "title" in args:
            book.title = args['title']
        if "author" in args:
            book.author = args['author']
        if "read" in args:
            book.read = args['read']
        db.session.add(book)
        db.session.commit()
        return book, 200


class CreateBook(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = book_put_args.parse_args()
        book = BookModel(id=uuid4().hex,title=args["title"],author=args["author"],read=args["read"])
        db.session.add(book)
        db.session.commit()
        return book, 201
    

api.add_resource(Books,"/api/v1/books")
api.add_resource(CreateBook,"/api/v1/book/create")
api.add_resource(Book,"/api/v1/book/<string:book_id>")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host="0.0.0.0",port=5000,debug=True)
