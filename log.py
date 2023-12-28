import time as times
import db

def newLog(ip:str,tokens:int, model:str, userkey:str):
    db.newLog(ip, int(times.time()), tokens, model, userkey)

def getlog(num:int):
    if num < 0:
        num = 10
    rawdata = db.getlog(num)
    data = []
    for i in rawdata:
        item = list(i)
        item[1] = times.strftime("%Y-%m-%d %H:%M:%S",times.localtime(i[1]))
        data.append(item)

    return data

    