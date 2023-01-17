# ./apps/items/models.py

from apps.exts import db


class Items(db.Model):
    def __init__(self, key):
        self.__bind_key__ = key

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    info = db.Column(db.String(256), nullable=True)
    price = db.Column(db.Float, nullable=True, default='0')

    def __str__(self):
        return self.name
