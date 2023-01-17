# ./apps/supplier/view.py
import json
# .\apps\user\view.py

# 创建user的蓝图对象
from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from apps.supplier.models import Supplier
import hashlib
from apps.exts.create_database import create_database
from apps.items.models import Items, db
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

supplier_bp = Blueprint('supplier', __name__)


@supplier_bp.route('/supplier_center')
def supplier_center():
    return render_template('supplier/supplier_center.html')


@supplier_bp.route('/supplier_login', methods=['GET', 'POST'])
def supplier_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_password = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()
        user_list = Supplier.query.filter_by(username=username)
        for user in user_list:
            if user.password == new_password and user.identity == 'supplier':
                session['username'] = username
                session['password'] = password
                return redirect(url_for('supplier.supplier_center'))
                # return render_template('supplier/supplier_center.html', username=username)
            else:
                flash('用户名或密码错误')
                return render_template('supplier/supplier_login.html')
        flash('用户名或密码错误')
        return render_template('supplier/supplier_login.html')
    return render_template('supplier/supplier_login.html')


# @supplier_bp.route('/supplier_register', methods=['GET', 'POST'])
# def supplier_register_page():
#     return render_template('supplier/supplier_register.html')


# 获取注册信息
@supplier_bp.route('/supplier_register', methods=['GET', 'POST'])
def supplier_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # print(password)
        repassword = request.form.get('repassword')
        if password == repassword:
            supplier = Supplier()  # 实例化user对象
            supplier.identity = 'supplier'
            supplier.username = username
            supplier.password = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()
            db.session.add(supplier)
            db.session.commit()
            create_database(username)  # 创建各个企业的数据库

            # 存储企业数据库信息
            tf = open("./data/database.json", 'r')
            my_dict = json.load(tf)
            tf.close()
            my_dict[username] = 'mysql+pymysql://root:123456@127.0.0.1:3306/'+username
            tf = open("./data/database.json", 'w')
            json.dump(my_dict, tf)
            tf.close()

            # 创建表
            # conn = pymysql.connect(host='localhost', user='root', password='123456')
            # cursor = conn.cursor()
            # cursor.execute('use '+username)
            # cursor.execute('create table "items"("name" varchar(10) not null ,"id" int auto_increment, \
            # "info" varchar(256), "price" float)')

            # 清除网页缓存
            session.clear()
            session['username'] = username
            session['password'] = password
            flash("注册成功")
            return render_template('supplier/supplier_center.html')
        else:
            return render_template('supplier/supplier_register.html')
    return render_template('supplier/supplier_register.html')


# 商品管理
@supplier_bp.route('/supplier_center/items')
def supplier_items():
    if request.method == 'GET':
        username = session.get('username')
        return render_template('supplier/supplier_items.html', username=username)
    return render_template('supplier/supplier_items.html')


@supplier_bp.route('/supplier_center/items/add', methods=['GET', 'POST'])
def item_add():
    if request.method == 'POST':
        username = session.get('username')
        item = Items(username)
        item.name = request.form.get('item_name')
        # conn = pymysql.connect(host='localhost', user='root', password='123456')
        # cursor = conn.cursor()
        # cursor.execute('use '+session.get('username'))
        # cursor.execute('create table "items" ("name" VARCHAR(11));')

        # 连接到企业的数据库并传入商品信息
        engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/'+username)
        Session = sessionmaker(bind=engine)
        sess = Session()
        sess.add(item)
        sess.commit()
        print('ok')
        flash('添加成功')
        return render_template('supplier/supplier_items.html', username=username)
    return render_template('supplier/supplier_items.html')
