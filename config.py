import json

def readConf():
    with open('config.json') as f:
        return json.load(f)

def updateConf(data_dict):
    # 打开JSON文件并读取内容
    file_path = 'config.json'
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # 将新的数据合并到现有的数据中
    existing_data.update(data_dict)

    # 再次打开文件（这次是以写模式），并将更新后的数据保存回文件
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4, ensure_ascii=False)

