"""
coding:utf-8
@Software:PyCharm
@Time:2022/12/16 20:11
@Author:庸人
"""
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from iwater.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 以下是认证方面的视图
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = '用户名必填！'
        elif not password:
            error = '密码必填！'
        elif db.execute(
                'SELECT id FROM app_user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = '用户 {} 已经注册！'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO app_user (username,password) Values (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM app_user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '用户名错误！'
        elif not check_password_hash(user['password'], password):
            error = '密码错误！'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM app_user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 在其他视图中验证--必须登录
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


# 在其他视图中验证--必须管理员admin
def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['id'] != '1':
            flash('必须是超级管理员')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


