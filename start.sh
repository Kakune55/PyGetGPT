#!/bin/bash

# 定义要运行的Python文件
PYTHON_APP="main.py"

# 使用nohup命令启动Python程序，并将其输出重定向到日志文件
nohup python3 $PYTHON_APP > output.log 2>&1 &

# 打印消息，通知用户程序已启动
echo "Python application started!"

# 可以添加任何其他需要的启动逻辑
