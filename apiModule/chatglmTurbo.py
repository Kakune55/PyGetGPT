import zhipuai , config

zhipuai.api_key = config.readConf()["chatglmturbo"]["Authorization"]

def service(prompt,history = ""):
    if history == "":
        response = zhipuai.model_api.invoke(
            model="chatglm_turbo",
            prompt=[
                {"role": "user", "content": prompt},
            ]
        )
    else:
        response = zhipuai.model_api.invoke(
            model="chatglm_turbo",
            prompt=[
                {"role": "user", "content": history[1]["user"]},
                {"role": "assistant", "content": history[1]["bot"]},
                {"role": "user", "content": history[0]["user"]},
                {"role": "assistant", "content": history[0]["bot"]},
                {"role": "user", "content": prompt},
            ]
        )
    if response["code"] == 200:
        return 200, str(response["data"]["choices"][0]["content"]).split('"')[1], response["data"]["usage"]['total_tokens']
    else:
        return 50 , str(response["code"])+response["msg"], 0
