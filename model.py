from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields

db = SQLAlchemy(app)
ma = Marshmallow(app)

class BookModel(db.Model):
    id = db.Column(db.String(50),primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    author = db.Column(db.String(100),nullable=False)
    read = db.Column(db.Boolean)
    

class BookModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BookModel
        load_instance = True
        Ordered = True
