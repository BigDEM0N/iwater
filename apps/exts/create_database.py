# ./apps/exts/create_database.py
import pymysql
import traceback


def create_database(name):
    conn = pymysql.connect(host='localhost', user='root', password='123456')
    cursor = conn.cursor()
    try:
        cursor.execute('create database %s' % name)  # 建库
        cursor.execute('use ' + name)   # 建表
        sql = '''
        create table items(
            name varchar(10) not null,
            id int auto_increment,
            info varchar(256),
            price float, primary key (id))
        '''
        cursor.execute(sql)
    except Exception:
        f = open("./data/database_log.txt", 'a')  # 将异常信息写入日志文件中
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        conn.rollback()
    finally:
        conn.close()
    return 'ok'


def create_supplier_table():  # 创建存储企业用户的数据表
    conn = pymysql.connect(host='localhost', user='root', password='123456')
    try:
        cursor = conn.cursor()
        cursor.execute('use db_user')
        # 存储企业的名称、id、信息、是否提供服务、是否启用、地址、图像
        sql = '''
        create table if not exists supplier(
                        username varchar(64) not null,
                        password varchar(256) not null,
                        id int auto_increment,
                        info varchar(256),
                        server_on bool default 0,
                        isvalid bool default 1,
                        address varchar(256),
                        icon varchar(256),
                        identity varchar(64),
                        primary key(id))
        '''
        cursor.execute(sql)
    except Exception:
        f = open("./data/database_log.txt", 'a')  # 将异常信息写入日志文件中
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        conn.rollback()
        return False
    finally:
        conn.close()

    return True


def create_customer_table():  # 创建存储用户的数据表
    conn = pymysql.connect(host='localhost', user='root', password='123456')
    try:
        cursor = conn.cursor()
        cursor.execute('use db_user')
        sql = '''
            create table if not exists customer(
                        username varchar(64) not null,
                        password varchar(256) not null,
                        id int auto_increment,
                        info varchar(256), server_on bool default 0,
                        isvalid bool default 1, address varchar(256),
                        icon varchar(256), primary key(id),
                        identity varchar(64))
        '''
        cursor.execute(sql)
        print('good')
    except Exception:
        f = open("./data/database_log.txt", 'a')  # 将异常信息写入日志文件中
        traceback.print_exc(file=f)
        f.flush()
        f.close()
        conn.rollback()
        return False  # 异常则返回失败
    finally:
        conn.close()

    return True
