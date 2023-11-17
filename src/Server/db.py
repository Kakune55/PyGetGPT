import pymysql , config


def userSurplus(userkey):
    #打开数据库连接
    db = pymysql.connect(host=config.readConf()["db"]["host"],
                     port=config.readConf()["db"]["port"],
                     user=config.readConf()["db"]["user"],
                     password=config.readConf()["db"]["passwd"],
                     database=config.readConf()["db"]["database"])
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
 
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute(f"SELECT surplus FROM usersurplus WHERE userkey = '{userkey}';")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    # 关闭连接
    db.close()

    if data != None:
        return data[0]
    return -99999

def reduce_value(userkey, value):  # 减去对应的值
    #打开数据库连接
    db = pymysql.connect(host=config.readConf()["db"]["host"],
                    port=config.readConf()["db"]["port"],
                    user=config.readConf()["db"]["user"],
                    password=config.readConf()["db"]["passwd"],
                    database=config.readConf()["db"]["database"])
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 执行 SQL 查询以获取当前值
    cursor.execute(f"SELECT surplus FROM usersurplus WHERE userkey = '{userkey}';")
    current_value = cursor.fetchone()[0]

    # 如果没有找到用户，则返回错误信息
    if current_value is None:
        db.close()
        return -1

    # 计算新的值
    new_value = current_value - value

    # 更新数据库中的值
    cursor.execute(f"UPDATE usersurplus SET surplus={new_value} WHERE userkey='{userkey}'")

    # 提交事务
    db.commit()

    # 关闭连接
    db.close()

    # 返回新值
    return 0