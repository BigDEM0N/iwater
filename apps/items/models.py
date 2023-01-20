# ./apps/items/models.py

from apps.exts import db
import datetime


class Items(db.Model):
    def __init__(self, key):
        self.__bind_key__ = key

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    info = db.Column(db.String(256), nullable=True)
    price = db.Column(db.Float, nullable=True, default='0')

    def __str__(self):
        return self.name


class Order(db.Model):
    def __init__(self, key):
        self.__bind_key__ = key

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String(256))  # 字典转string
    customer = db.Column(db.String(64))
    supplier = db.Column(db.String(64))
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    amount = db.Column(db.Float, nullable=False, default=0)

    def __str__(self):
        return '订单号：'+self.num
