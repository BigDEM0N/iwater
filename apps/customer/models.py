# ./apps/customer/models.py

from apps.user.models import User
from apps.exts import db


class Customer(User):
    pass
    # identity = db.Column(db.String(10), nullable=False)
