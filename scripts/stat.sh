#!/bin/bash

cd $PROJECT_ROOT
python -m venv venv
source venv/bin/activate
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install wheel hdfs

python codes/dormlog_stat.py
