# .\settings

import json

if open("./data/database.json", "r"):
    tf = open("./data/database.json", "r")  # 读入数据库
    print(tf)
    db_binds = json.load(tf)
else:
    db_binds = {}


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/db_user'
    SQLALCHEMY_DATABASE_BINDS = db_binds
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = '123456'


class DevelopmentConfig(Config):
    ENV = 'development'


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
