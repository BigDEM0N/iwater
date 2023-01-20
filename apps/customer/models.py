# ./apps/customer/models.py

from apps.exts import db


class Customer(db.Model):
    __table_name__ = 'customer'
    identity = db.Column(db.String(64))
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    info = db.Column(db.String(256))
    isvalid = db.Column(db.BOOLEAN, default=True)
    address = db.Column(db.String(256))
    icon = db.Column(db.String(256))

    def __str__(self):
        return self.username
