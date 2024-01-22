from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from uuid import uuid4

from misc import book_put_args, checkBook

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdatabase.db"

from model import db, BookModel, BookModelSchema

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'  

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)




books_schema = BookModelSchema(many=True)
book_schema = BookModelSchema()



class Books(Resource):
    def get(self):
        books = BookModel.query.all()
        return jsonify(books_schema.dump(books))


class Book(Resource):
    def get(self,book_id):
        book = BookModel.query.get(book_id)
        checkBook(book)
        return jsonify(book_schema.dump(book))
    
    def delete(self,book_id):
        book = BookModel.query.get(book_id)
        checkBook(book)
        db.session.delete(book)
        db.session.commit()
        return {"message":"book has been deleted","code":204}
    
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
        print(book)
        return jsonify(book_schema.dump(book))


class CreateBook(Resource):
    def post(self):
        args = book_put_args.parse_args()
        book = BookModel(id=uuid4().hex,title=args["title"],author=args["author"],read=args["read"])
        db.session.add(book)
        db.session.commit()
        return jsonify(book_schema.dump(book))


api.add_resource(Books,"/api/v1/books")
api.add_resource(CreateBook,"/api/v1/book/create")
api.add_resource(Book,"/api/v1/book/<string:book_id>")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host="0.0.0.0",port=5000,debug=True)
