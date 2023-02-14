# ./apps/supplier/view.py
from flask import render_template, request, flash, session, url_for, redirect, Blueprint
from apps.supplier.models import Supplier
import hashlib
from apps.exts.create_database import create_database, create_supplier_table
from apps.exts.dbinfo_save import dbinfo_save
from apps.items.models import Items
import pymysql
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

# 创建supplier的蓝图对象
supplier_bp = Blueprint('supplier', __name__)


@supplier_bp.route('/supplier_center')
def supplier_center():
    identity = session.get('identity')
    username = session.get('username')
    if identity == 'supplier':
        supplier_list = Supplier.query.filter_by(username=username)
        supplier = supplier_list[0]
        if supplier.server_on:
            conn = pymysql.connect(host='localhost', user='root', password='123456')
            try:
                cursor = conn.cursor()
                cursor.execute('use ' + username)
                sql = '''
                    select * from items;
                '''
                cursor.execute(sql)
                conn.commit()
                item_list = cursor.fetchall()
                print(item_list)
            except Exception:
                f = open("./data/database_log.txt", 'a')  # 将异常信息写入日志文件中
                traceback.print_exc(file=f)
                f.flush()
                f.close()
                conn.rollback()
            finally:
                conn.close()
                return render_template('supplier/supplier_center.html', item_list=item_list, username=username)
        else:
            flash('未开启服务')
            return redirect(url_for('supplier.supplier_login'))
    else:
        flash('暂无权限!')
        'error'
        return redirect(url_for('supplier.supplier_login'))


@supplier_bp.route('/supplier_login', methods=['GET', 'POST'])
def supplier_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_password = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()
        user_list = Supplier.query.filter_by(username=username)
        for user in user_list:
            if user.password == new_password and user.identity == 'supplier':
                session.clear()
                session['username'] = username
                session['password'] = password
                session['identity'] = user.identity
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
            # 创建各个企业的数据库 #转到admin页面

            # 存储企业数据库信息
            dbinfo_save(username)

            # 清除网页缓存
            session.clear()
            session['username'] = username
            session['password'] = password
            flash("注册成功")
            return redirect(url_for('supplier.supplier_center'))
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
        item.name = request.form.get('name')
        item.info = request.form.get('info')
        item.price = request.form.get('price')
        item.num = username + str(time.time())  # 获得当前时间
        print(item.num)
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
        return redirect(url_for('supplier.supplier_center'))
    return render_template('supplier/supplier_center.html')


@supplier_bp.route('/supplier_center/items/upgrade', methods=['POST', 'GET'])
def item_upgrade():
    if request.method == 'GET':
        name = request.args.get('name')
        id = request.args.get('id')
        info = request.args.get('info')
        price = request.args.get('price')
        session['id'] = id
        print(id)
    if request.method == 'POST':
        username = session.get('username')
        name = request.form.get('name')
        info = request.form.get('info')
        price = request.form.get('price')
        conn = pymysql.connect(host='localhost', user='root', password='123456')
        try:
            cursor = conn.cursor()
            cursor.execute('use ' + username)
            sql = "update items set name='%s' where id='%s'" % (name, session.get('id'))
            print(sql)
            cursor.execute(sql)
            sql = "update items set info='%s' where id='%s'" % (info, session.get('id'))
            cursor.execute(sql)
            sql = "update items set price='%s' where id='%s'" % (price, session.get('id'))
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
            return redirect(url_for('supplier.supplier_center'))
    return render_template('supplier/item_upgrade.html', name=name, id=id, info=info, price=price)


