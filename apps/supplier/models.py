# ./apps/supplier/models.py

from apps.exts import db
from apps.user.models import User


class Supplier(db.Model):
    # supplier_name = db.Column(db.String(64), nullable=False)
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    __table_name__ = 'suppliers'
    identity = db.Column(db.String(64))
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    info = db.Column(db.String(256))
    server_on = db.Column(db.BOOLEAN, default=False)
    isvalid = db.Column(db.BOOLEAN, default=True)
    address = db.Column(db.String(256))
    icon = db.Column(db.String(256))

    def __str__(self):
        return self.username
