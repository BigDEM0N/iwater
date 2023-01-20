# ./apps/supplier/view.py
from flask import render_template, request, flash, session, url_for, redirect,Blueprint
from apps.supplier.models import Supplier
import hashlib
from apps.exts.create_database import create_database, create_supplier_table
from apps.exts.dbinfo_save import dbinfo_save
from apps.items.models import Items
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 创建supplier的蓝图对象
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

            # 创建数据表
            if create_supplier_table():
                pass
            else:
                flash("注册错误，请联系管理员 error:01")
                return render_template('supplier/supplier_register.html')

            # 验证用户名唯一
            user_list = Supplier.query.all()
            for user in user_list:
                if username == user.username:
                    flash("该用户名已被使用")
                    return render_template('supplier/supplier_register.html')
                else:
                    pass

            # 实例化user对象
            supplier = Supplier()
            supplier.identity = 'supplier'
            supplier.username = username
            supplier.password = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()

            # 提交企业信息至suppliers数据表
            engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/db_user')
            Session = sessionmaker(bind=engine)
            sess = Session()
            sess.add(supplier)
            sess.commit()
            # db.session.add(supplier)
            # db.session.commit()
            create_database(username)  # 创建各个企业的数据库 #转到admin页面

            # 存储企业数据库信息
            dbinfo_save(username)

            # 清除网页缓存
            session.clear()
            session['username'] = username
            session['password'] = password
            flash("注册成功")
            return render_template('supplier/supplier_center.html')
        else:
            flash("两次输入的密码不一致")
            return render_template('supplier/supplier_register.html')
    else:
        pass
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
