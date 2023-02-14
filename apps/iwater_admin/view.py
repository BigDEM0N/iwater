# ./apps/iwater_admin/view.py

from flask import render_template, request, flash, redirect, url_for, session, Blueprint
from apps.iwater_admin.models import Admin
from apps.supplier.models import Supplier
import pymysql
import hashlib
from apps.exts import db
import json
import traceback
from apps.exts.create_database import create_database

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
                session.clear()
                session['username'] = username
                session['identity'] = admin.identity
                return redirect(url_for('admin.supplier_manage'))
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
            session['identity'] = admin.identity
            flash("注册成功")
            return redirect(url_for('admin.admin_center'))
        else:
            return render_template('admin/admin_register.html')
    return render_template('admin/admin_register.html')


@admin_bp.route('/admin/supplier_manage')
def supplier_manage():
    identity = session.get('identity')
    if identity == 'admin':
        supplier_list = Supplier.query.all()
        return render_template('admin/manage.html', supplier_list=supplier_list)
    else:
        flash('暂无权限 请登录')
        return redirect(url_for('admin.admin_login'))


@admin_bp.route('/admin/supplier_manage/details')
def supplier_details():
    ID = request.args.get('id')
    supplier_list = Supplier.query.filter_by(id=ID)
    supplier = supplier_list[0]

    return render_template('admin/supplier_details.html', supplier=supplier)


@admin_bp.route('/admin/supplier_activate')
def supplier_activate():
    identity = session.get('identity')
    if identity == "admin":
        id = request.args.get('id')
        supplier_list = Supplier.query.filter_by(id=id)
        conn = pymysql.connect(host='localhost', user='root', password='123456', database="db_user")
        cursor = conn.cursor()
        try:
            sql = "update supplier set server_on='1' where id='%s'" % id
            cursor.execute(sql)
            conn.commit()
        except Exception:
            f = open("./data/database_log.txt", 'a')  # 将异常信息写入日志文件中
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            conn.rollback()
        finally:
            conn.close()
        create_database(supplier_list[0].username)
        return redirect(url_for('admin.supplier_manage'))
    else:
        flash('暂无权限 请登录')
        return redirect(url_for('admin.admin_login'))


@admin_bp.route('/admin/supplier_offline')
def supplier_offline():
    identity = session.get('identity')
    if identity == 'admin':
        id = request.args.get('id')
        supplier_list = Supplier.query.filter_by(id=id)
        conn = pymysql.connect(host='localhost', user='root', password='123456', database="db_user")
        cursor = conn.cursor()
        try:
            sql = "update supplier set server_on='0' where id='%s'" % id
            cursor.execute(sql)
            conn.commit()
        except Exception:
            f = open("./data/database_log.txt", 'a')  # 将异常信息写入日志文件中
            traceback.print_exc(file=f)
            f.flush()
            f.close()
            conn.rollback()
        finally:
            conn.close()
        create_database(supplier_list[0].username)
        return redirect(url_for('admin.supplier_manage'))
    else:
        flash('暂无权限 请登录')
        return redirect(url_for('admin.admin_login'))
