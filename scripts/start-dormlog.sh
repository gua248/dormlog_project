#!/bin/bash

echo "==== build python venv ===="
cd $PROJECT_ROOT
python -m venv venv
source venv/bin/activate
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install wheel
pip install -r requirements.txt

sleep 3
echo "==== start dormlog ===="
cd $PROJECT_ROOT/codes
nohup spark-submit --jars $SPARK_HOME/jars/spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar dormlog_spark.py >/dev/null 2>&1 &
sleep 3
nohup python dormlog_producer.py &
