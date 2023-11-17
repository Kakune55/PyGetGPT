import requests , json , config

# 设置请求的目标URL
url = config.readConf()["qwenturbo"]["url"]  # 替换为你的API端点URL
header = {
    "Content-Type":"application/json",
    "Authorization":config.readConf()["qwenturbo"]["Authorization"]
}

def service(prompt,history = ""):
    # 设置请求数据
    if history == "":
        data = {
            "model": "qwen-turbo",
            "input":{
                "prompt":f"{prompt}"
            }
        }
    else:
        data = {
            "model": "qwen-turbo",
            "input":{
                "prompt":f"{prompt}",
                "history":history
            }
        }
    # 发送POST请求
    response = json.loads(requests.post(url, json=data ,headers=header).text)
    if 'code' in response:
        return 50,response['code']+response['message'],0
    return 200,response['output']['text'],response["usage"]["total_tokens"]