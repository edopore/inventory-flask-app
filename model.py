from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class BookModel(db.Model):
    id = db.Column(db.String(50),primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    author = db.Column(db.String(100),nullable=False)
    read = db.Column(db.Boolean)

    def __repr__(self):
        return f"{self.id} : {self.title} written by {self.author}"