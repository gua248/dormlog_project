from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import traceback
import json


def dormlog_producer():
    # 假设生产的消息为键值对（不是一定要键值对），且序列化方式为json
    path = '../2021-09-03online-dorm.log'
    producer = KafkaProducer(bootstrap_servers=['node1:9092', 'node2:9092', 'node3:9092'])
    # 发送消息
    with open(path, 'rb') as f:
        for line in f.readlines():
            future = producer.send('dormlog', line)
            try:
                future.get(timeout=10)  # 监控是否发送成功
            except kafka_errors:  # 发送失败抛出kafka_errors
                traceback.format_exc()


def consumer_demo():
    consumer = KafkaConsumer(
        'dormlog',
        bootstrap_servers='node1:9092,node2:9092,node3:9092',
        group_id='test'
    )
    for message in consumer:
        print("receive, {}".format(message))


if __name__ == '__main__':
    dormlog_producer()
