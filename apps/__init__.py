# .\apps\__init__.py

from flask import Flask, session
from flask_session import Session
from apps.user.view import user_bp
from apps.iwater_admin.view import admin_bp
from apps.supplier.view import supplier_bp
from apps.customer.view import customer_bp
from apps.exts import db
from apps.exts.create_database import create_supplier_table

import settings


def creat_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # app.config['SESSION_KEY'] = '123'  # Set the secret_key on the 报错

    app.config.from_object(settings.DevelopmentConfig)
    db.init_app(app)

    # 将db对象与app进行关联
    app.register_blueprint(customer_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(supplier_bp)
    return app
