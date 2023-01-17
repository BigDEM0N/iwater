# ./apps/iwater_admin/models.py

from apps.exts import db
from apps.user.models import User


class Admin(User):
    pass
    # identity = db.Column(db.String(10), nullable=False)
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name = db.Column(db.String(11), nullable=False, unique=True)
    # password = db.Column(db.String(256), nullable=False)
