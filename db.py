
from flask_login import  UserMixin
from config import db

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Goods(db.Model,JsonModel,UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key = True)
    name =  db.Column(db.String(300),nullable = False)
    title =  db.Column(db.String(300),nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    def __repr__(self):
        return '<Goods %r>' % self.id

class Orders(db.Model,JsonModel,UserMixin):


    id = db.Column(db.Integer,primary_key = True)
    product_id =  db.Column(db.String(10), nullable = False)
    amount = db.Column(db.String(10), nullable = False)
    email = db.Column(db.String(50),nullable = False)
    date = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return '<Goods %r>' % self.id
