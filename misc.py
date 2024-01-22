from flask_restful import reqparse, abort


book_put_args = reqparse.RequestParser()
book_put_args.add_argument("title",type=str,help="Title of book")
book_put_args.add_argument("author",type=str,help="Name of the book's author")
book_put_args.add_argument("read",type=bool,help="Define if book was read or not")


def checkBook(book):
    if not book:
        abort(404,message="Book does not exists :c")

