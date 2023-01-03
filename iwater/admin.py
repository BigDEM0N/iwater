"""
coding:utf-8
@Software:PyCharm
@Time:2022/12/29 19:23
@Author:庸人
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from iwater.auth import admin_required
from iwater.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


# 后台首页
@bp.route('/')
@admin_required
def index():
    db = get_db()
    users = db.execute(
        'SELECT * FROM app_user'
    ).fetchall()
    if users is None:
        flash('库中还没有用户！')
    return render_template('admin/index.html', users=users)

