"""
coding:utf-8
@Software:PyCharm
@Time:2022/12/30 21:33
@Author:庸人
"""
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from iwater.auth import login_required
from iwater.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/user/')
@login_required
def get_user_info():
    db = get_db()
    error = None
    result = db.execute(
        'SELECT * FROM app_user'
    ).fetchall()
    return result

