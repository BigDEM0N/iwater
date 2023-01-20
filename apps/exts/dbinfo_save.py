# ./apps/exts/dbinfo_save.py
import json


def dbinfo_save(username):
    # 存储企业数据库信息
    try:
        tf = open("./data/database.json", 'r')
        my_dict = json.load(tf)
        tf.close()
        my_dict[username] = 'mysql+pymysql://root:123456@127.0.0.1:3306/' + username
        tf = open("./data/database.json", 'w')
        json.dump(my_dict, tf)
        tf.close()
    except Exception:
        return False  # 异常则返回失败

    return True
