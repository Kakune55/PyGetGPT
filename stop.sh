#!/bin/bash

# 定义要停止的Python文件
PYTHON_APP="main.py"

# 使用ps命令查找Python进程，并使用grep过滤出要停止的进程
PID=$(ps -ef | grep $PYTHON_APP | grep -v grep | awk '{print $2}')

# 检查是否找到了进程
if [ -z "$PID" ]; then
    echo "Python application is not running!"
else
    # 使用kill命令停止进程
    kill $PID
    echo "Python application stopped!"
fi

# 可以添加任何其他需要的停止逻辑
