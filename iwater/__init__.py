"""
coding:utf-8
@Software:PyCharm
@Time:2022/12/16 20:10
@Author:庸人
"""
import os
from flask import Flask, escape, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=b'\xaf\xcd\xe8U\xd9\x86\x95\x94K_\xc2\xed\xa2\xd08\x0f',
        DATABASE=os.path.join(app.instance_path, 'iwater.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/user/<username>')
    def profile(username):
        return '{}\'s profile'.format(escape(username))

    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)


    # 注册数据库初始化
    from . import db
    db.init_app(app)

    # 注册auth认证 蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)
    app.add_url_rule('/', endpoint='index')

    from . import api
    app.register_blueprint(api.bp)

    return app
