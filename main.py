import flask
from flask_cors import CORS
import db , config , log
from apiModule import qwenTurbo , chatglmTurbo , gpt35Turbo , gpt4Turbo

app = flask.Flask(__name__)
CORS(app,origins="*")
app.secret_key = b'SQ-{kJE;m(jEBi|{yq]v'
app.config['TRUSTED_PROXIES'] = ['proxy_ip']

@app.route('/api/user', methods=['POST'])
def post_data():
    userRequest = flask.request.json
    surplusToken = db.userSurplus(userRequest['userkey'])

    if userRequest["prompt"] == "":
        return {"code":42,"output":"Input is empty"}
    
    if userRequest["prompt"] == "":
        return {"code":42,"output":"UserKey is empty"}

    if surplusToken == -99999: # 判断用户是否存在和余额
        return {"code":41,"output":"UserKey not found"}
    elif surplusToken <= 0:
        return {"code":40,"output":"Token has been use up"}
    
    if userRequest["model"] == "qwen-turbo": # 调用qwen-Turbo
        if userRequest["context"] == 1: # 是否使用上文关联
            code , output , tokenUsed = qwenTurbo.service(userRequest['prompt'],userRequest['history'])
        elif userRequest["context"] == 0:
            code , output , tokenUsed = qwenTurbo.service(userRequest['prompt'])

    if userRequest["model"] == "chatglm-turbo": # 调用chatglm-turbo
        if userRequest["context"] == 1: # 是否使用上文关联
            code , output , tokenUsed = chatglmTurbo.service(userRequest['prompt'],userRequest['history'])
        elif userRequest["context"] == 0:
            code , output , tokenUsed = chatglmTurbo.service(userRequest['prompt'])

    if userRequest["model"] == "gpt3.5-turbo": # 调用gpt3.5-turbo
        if userRequest["context"] == 1: # 是否使用上文关联
            code , output , tokenUsed = gpt35Turbo.service(userRequest['prompt'],userRequest['history'])
        elif userRequest["context"] == 0:
            code , output , tokenUsed = gpt35Turbo.service(userRequest['prompt'])

    if userRequest["model"] == "gpt4.0-turbo": # 调用gpt4.0-turbo
        if userRequest["context"] == 1: # 是否使用上文关联
            code , output , tokenUsed = gpt4Turbo.service(userRequest['prompt'],userRequest['history'])
        elif userRequest["context"] == 0:
            code , output , tokenUsed = gpt4Turbo.service(userRequest['prompt']) 

    db.reduce_value(userRequest['userkey'], tokenUsed)
    log.newLog(flask.request.headers.get('X-Forwarded-For'), tokenUsed, userRequest["model"], userRequest['userkey'])
    return {"code":code,"output":output,"surplus":surplusToken}


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    userRequest = flask.request.form
    if userRequest["password"] != config.readConf()["adminkey"]:
        return flask.render_template('login.html')
    flask.session["admin"] = True
    return flask.redirect(flask.url_for('admin'))


@app.route('/admin')
def admin():
    if "admin" in flask.session :
        status = {}
        status["db"] = db.dbIsOK()
        return flask.render_template("status.html" ,status=status)
    return flask.redirect('login')


@app.route('/admin/list')
def adminList():
    if "admin" in flask.session :
        data = db.getAllKey()
        return flask.render_template("keylist.html",data=data)
    return flask.redirect('login')

@app.route('/admin/log', methods=['GET'])
def adminListLog():
    if "admin" in flask.session :
        if 'show' in flask.request.args:
            try:
                shownum = int(flask.request.values.get('show'))
            except:
                return flask.abort(400)
        else:
            return flask.abort(400)
        data = log.getlog(shownum)
        return flask.render_template("loglist.html",data=data)
    return flask.redirect('login')

@app.route('/admin/createkey', methods=['POST','GET'])
def createkey():
    if "admin" in flask.session :
        if flask.request.method == "GET":
            return flask.render_template("createKey.html",resq="null")
        if  "number" in flask.request.form: # 创建单个还是多个
            resq = db.createKey(flask.request.form["quota"], flask.request.form["number"])
        elif "key" in flask.request.form:
            resq = db.createKey(flask.request.form["quota"],1,flask.request.form["key"])

        return flask.render_template("createKey.html",resq=resq)
    return flask.redirect('login')

@app.route('/admin/lookupkey', methods=['POST','GET'])
def lookupkey():
    if "admin" in flask.session :
        if flask.request.method == "GET":
            return flask.render_template("lookupKey.html",resq="null")
        resq = db.userSurplus(flask.request.form["key"])
        return flask.render_template("lookupKey.html",resq=resq)
    return flask.redirect('login')

@app.route('/admin/operate', methods=['POST','GET'])
def operate():
    if "admin" in flask.session :
        if flask.request.args['type'] == "del":
            if db.delKey(flask.request.args['target']):
                return "成功 <a href='javascript:;' onclick='self.location=document.referrer;'>返回上一页并刷新</a>"
            return "失败 <a href='javascript:;' onclick='self.location=document.referrer;'>返回上一页并刷新</a>"
    return "拒绝访问"


if __name__ == '__main__':
    app.run(debug=bool(config.readConf()["appconf"]["debug"]),host=config.readConf()["appconf"]["host"],port=config.readConf()["appconf"]["port"])