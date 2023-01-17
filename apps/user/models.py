# .\apps\user\models.py

from apps.exts import db
import datetime


class User(db.Model):  # 继承
    # db.Column(类型，约束) 映射表中的类
    identity = db.Column(db.String(64), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary_key 主键	autoincrement 自增
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    # phone = db.Column(db.String(11), unique=True)
    rdatetime = db.Column(db.DateTime, default=datetime.datetime.now())

    def __str__(self):
        return self.username


# class Userinfo(db.Model):
#     pass
