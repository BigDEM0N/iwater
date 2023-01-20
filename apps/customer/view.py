# ./apps/customer/view.py
from apps.customer.models import Customer
from flask import render_template, request, flash, session, url_for, redirect, Blueprint
import hashlib
from apps.exts.create_database import create_customer_table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 创建customer的蓝图对象
customer_bp = Blueprint('customer', __name__)


# 用户注册
@customer_bp.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if password == repassword:

            # 创建数据表
            if create_customer_table():
                pass
            else:
                flash("注册错误，请联系管理员 error:01")
                return render_template('customer/customer_register.html')

            # 验证用户名唯一
            user_list = Customer.query.all()
            for user in user_list:
                if username == user.username:
                    flash("该用户名已被使用")
                    return render_template('supplier/supplier_register.html')
                else:
                    pass

            # 实例化customer对象
            customer = Customer()
            customer.identity = 'customer'
            customer.username = username
            customer.password = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()

            # 提交用户注册信息
            engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/db_user')
            Session = sessionmaker(bind=engine)
            sess = Session()
            sess.add(customer)
            sess.commit()

            # 网页session存储用户信息
            session.clear()     # 注册之后清除之前的用户信息
            session['username'] = username
            session['password'] = password
            flash("注册成功")
            return redirect(url_for('customer.customer_center'))
        else:
            flash("两次输入的密码不一致")
            return render_template('customer/customer_register.html')
    else:
        pass
    return render_template('customer/customer_register.html')


@customer_bp.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_password = hashlib.sha256(str(password).encode(encoding='utf-8')).hexdigest()
        user_list = Customer.query.filter_by(username=username)
        for user in user_list:
            if user.password == new_password and user.identity == 'customer':
                session['username'] = username
                session['password'] = password
                return redirect(url_for('customer.customer_center'))
                # return render_template('supplier/supplier_center.html', username=username)
            else:
                flash('用户名或密码错误')
                return render_template('customer/customer_login.html')
        flash('用户名或密码错误')
        return render_template('customer/customer_login.html')
    return render_template('customer/customer_login.html')


@customer_bp.route('/customer_center')
def customer_center():
    return render_template('customer/customer_center.html')


@customer_bp.route('/market')
def customer_market():
    if request.method == 'POST':
        pass

    return render_template('customer/market.html')
