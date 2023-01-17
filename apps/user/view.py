# .\apps\user\view.py

# 创建user的蓝图对象
from flask import Blueprint, render_template, request, flash
from apps.user.models import User
import hashlib
from apps.exts import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/user_center')
def user_center():
    return '用户中心'


@user_bp.route('/user_login')
def user_login():
    return '用户登录'


@user_bp.route('/user_register', methods=['GET', 'POST'])
def user_register_page():
    return render_template('user/user_register.html')


# 获取注册信息
@user_bp.route('/user_register/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if password == repassword:
            user = User() # 实例化user对象
            user.username = username
            user.identity = 'customer'
            user.password = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()
            db.session.add(user)
            db.session.commit()
            flash("注册成功")
            return render_template('user/user_register.html')
        else:
            return render_template('user/user_register.html')
