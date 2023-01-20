# ./apps/iwater_admin/view.py

from flask import render_template, request, flash, redirect, url_for, session, Blueprint
from apps.iwater_admin.models import Admin
import hashlib
from apps.exts import db
import json

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin_center')
def admin_center():
    username = session.get('username')
    if open("./data/database.json"):
        tf = open("./data/database.json", "r")
        database_info = json.load(tf)
        # print(database_info)
        return render_template('admin/admin_center.html', databases=database_info)
    else:
        print("error")
    return render_template('admin/admin_center.html')


@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_paasword = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()
        admin_list = Admin.query.filter_by(username=username)
        for admin in admin_list:
            if admin.password == new_paasword and admin.identity == 'admin':
                return redirect(url_for('admin.admin_center'))
            else:
                flash('用户名或密码错误')
                return render_template('admin/admin_login.html')
        flash('用户名或密码错误')
        return redirect(url_for('admin.admin_login'))
    return render_template('admin/admin_login.html')


# @admin_bp.route('/admin_register', methods=['GET', 'POST'])
# def admin_register_page():
#     return render_template('admin/admin_register.html')


@admin_bp.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if password == repassword:
            admin = Admin()  # 实例化user对象
            admin.identity = 'admin'
            admin.username = username
            admin.password = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()
            db.session.add(admin)
            db.session.commit()
            session['username'] = username
            flash("注册成功")
            return redirect(url_for('admin.admin_center'))
        else:
            return render_template('admin/admin_register.html')
    return render_template('admin/admin_register.html')
