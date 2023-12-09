import flask , requests , json 
from flask_cors import CORS
import db , qwenTurbo , chatglmTurbo , gpt35Turbo 




app = flask.Flask(__name__)
CORS(app,origins="*")

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





    db.reduce_value(userRequest['userkey'], tokenUsed)
    return {"code":code,"output":output,"surplus":surplusToken}


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)