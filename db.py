import config , uuid

def getconn():
    try:
        if config.readConf()["db"]["type"] == "sqlite3":
            import sqlite3
            conn = sqlite3.connect("APPData.db")
        elif config.readConf()["db"]["type"] == "mysql":
            import pymysql
            conn = pymysql.connect(host=config.readConf()["db"]["host"],
                        port=config.readConf()["db"]["port"],
                        user=config.readConf()["db"]["user"],
                        password=config.readConf()["db"]["passwd"],
                        database=config.readConf()["db"]["database"])
        return conn
    except:
        print("DB ERROR")
        return 0
def dbIsOK():
    #打开数据库连接
    if "init" not in config.readConf():
        config.updateConf({"init" : True})
        init()
        
    try:
        getconn()
        return True
    except:
        return False
    
def init():
    #打开数据库连接
    db = getconn()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    #建表
    cursor.execute(
        '''
        CREATE TABLE usersurplus (
            userkey TEXT,
            surplus INT);
        ''')
    # 提交事务
    db.commit()

    # 关闭连接
    db.close()

def userSurplus(userkey): #查询userkey剩余配额
    #打开数据库连接
    db = getconn()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
 
    # 使用 execute()  方法执行 SQL 查询 
    if config.readConf()["db"]["type"] == "sqlite3":
        cursor.execute(f"SELECT surplus FROM usersurplus WHERE userkey = ?;",[userkey])
    else:
        cursor.execute(f"SELECT surplus FROM usersurplus WHERE userkey = %s;",[userkey])
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    # 关闭连接
    db.close()

    if data != None:
        return data[0]
    return -99999

def reduce_value(userkey, value):  # 减去对应的值
    #打开数据库连接
    db = getconn()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 执行 SQL 查询以获取当前值
    if config.readConf()["db"]["type"] == "sqlite3":
        cursor.execute(f"SELECT surplus FROM usersurplus WHERE userkey = ?;",[userkey])
    else:
        cursor.execute(f"SELECT surplus FROM usersurplus WHERE userkey = %s;",[userkey])
    current_value = cursor.fetchone()[0]

    # 如果没有找到用户，则返回错误信息
    if current_value is None:
        db.close()
        return -1

    # 计算新的值
    new_value = current_value - value

    # 更新数据库中的值
    if config.readConf()["db"]["type"] == "sqlite3":
        cursor.execute(f"UPDATE usersurplus SET surplus= ? WHERE userkey= ?;",[new_value,userkey])
    else:
        cursor.execute(f"UPDATE usersurplus SET surplus= %s WHERE userkey= %s;",[new_value,userkey])

    # 提交事务
    db.commit()

    # 关闭连接
    db.close()

    # 返回新值
    return 0

def getAllKey():
    #打开数据库连接
    db = getconn()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
 
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute(f"SELECT * FROM usersurplus ;")
    # 使用 fetchall() 方法获取结果集
    data = cursor.fetchall()

    # 关闭连接
    db.close()

    return data


def delKey(userkey):
    #打开数据库连接
    db = getconn()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
 
    # 使用 execute()  方法执行 SQL 查询 
    if config.readConf()["db"]["type"] == "sqlite3":
        cursor.execute(f"DELETE FROM usersurplus WHERE userkey = ?;", [userkey])
    else:
        cursor.execute(f"DELETE FROM usersurplus WHERE userkey = %s;", [userkey])

    # 提交事务
    db.commit()

    if cursor.rowcount > 0: 
        db.close()    # 使用 rowcount() 方法查询受影响行数
        return True
    db.close()
    return False


def createKey(quota,number=1,key="null"):
    #打开数据库连接
    db = getconn()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
 
    # 使用 execute()  方法执行 SQL 查询 
    output = []
    if config.readConf()["db"]["type"] == "sqlite3":
        if key == "null":
            for i in range(int(number)):
                key = str(uuid.uuid1())
                output.append(key)
                cursor.execute(f"INSERT INTO usersurplus (userkey,surplus) VALUES (?, ?);", [key, quota])
        else:
            cursor.execute(f"INSERT INTO usersurplus (userkey,surplus) VALUES (?, ?);", [key, quota])
            output.append(key)
    else:
        if key == "null":
            for i in range(int(number)):
                key = str(uuid.uuid1())
                output.append(key)
                cursor.execute(f"INSERT INTO usersurplus (userkey,surplus) VALUES (%s, %s);", [key, quota])
        else:
            cursor.execute(f"INSERT INTO usersurplus (userkey,surplus) VALUES (%s, %s);", [key, quota])
            output.append(key)


    # 提交事务
    db.commit()

    db.close()

    return output

