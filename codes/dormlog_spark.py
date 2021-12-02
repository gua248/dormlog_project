# import findspark
# findspark.init()
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
import re
import json
from hdfs.client import *
import time

log_format = re.compile(
    r'(?P<ip>\d+.\d+.\d+.\d+) - - '
    r'\[(?P<date>.*)\] '
    r'\"(?P<request>.*)\" '
    r'(?P<status>\d+) (?P<bytes>\d+) '
    r'\"(?P<referrer>.*)\" '
    r'\"(?P<agent>.*)\"'
)


def dormlog_spark():
    spark = SparkSession.builder.master('spark://node1:7077').appName('dormlog').getOrCreate()
    # .config('spark.yarn.archive', '../tools/spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar')
    sc = spark.sparkContext
    ssc = StreamingContext(sc, 5)
    brokers = "node1:9092,node2:9092,node3:9092"
    topic = 'dormlog'
    # raw = KafkaUtils.createStream(
    #     ssc, brokers, 'group1', {topic: 1}
    # )
    raw = KafkaUtils.createDirectStream(
        ssc, [topic], {"metadata.broker.list": brokers}
    )
    parsed = raw.map(parser)
    ip_cnt = parsed.map(lambda d: (d['ip'], 1)).reduceByKey(lambda a, b: a + b)
    device_cnt = parsed.map(lambda d: (d['device'], 1)).reduceByKey(lambda a, b: a + b)
    status_cnt = parsed.map(lambda d: (d['status'], 1)).reduceByKey(lambda a, b: a + b)
    bytes_cnt = parsed.map(lambda d: int(d['bytes'])).reduce(lambda a, b: a + b)
    # ip_cnt.pprint()
    # device_cnt.pprint()
    # status_cnt.pprint()
    bytes_cnt.pprint()
    bytes_cnt.foreachRDD(save_bytes)
    device_cnt.foreachRDD(lambda rdd: save_others(rdd, name='device'))
    ip_cnt.foreachRDD(lambda rdd: save_others(rdd, name='ip'))
    status_cnt.foreachRDD(lambda rdd: save_others(rdd, name='status'))

    ssc.start()
    ssc.awaitTermination()


def parser(line):
    line_dict = log_format.search(str(line)).groupdict()
    device = re.search(r'\((.*?);', line_dict['agent'])
    device = 'Unknown' if device is None else device.groups()[0]

    line_dict['device'] = device
    return line_dict


def save_bytes(rdd):
    client = Client("http://node3:9870", root='/')
    r = rdd.take(1)
    r = r[0] if r else 0
    client.write('/dormlog_project/result_bytes.txt',
                 data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+' --- {:>12d} bytes\n'.format(r),
                 append=True)


def save_others(rdd, name=''):
    client = Client("http://node3:9870", root='/')
    path = '/dormlog_project/result_' + name + '.txt'
    client.write(path,
                 data=time.strftime('-'*30 + "\n%Y-%m-%d %H:%M:%S\n" + '-'*30 + '\n', time.localtime()),
                 append=True)
    for r in rdd.collect():
        client.write(path, data=str(r)+'\n', append=True)


if __name__ == '__main__':
    client = Client("http://node3:9870", root='/')
    client.write('/dormlog_project/result_bytes.txt', data='', overwrite=True)
    client.write('/dormlog_project/result_ip.txt', data='', overwrite=True)
    client.write('/dormlog_project/result_device.txt', data='', overwrite=True)
    client.write('/dormlog_project/result_status.txt', data='', overwrite=True)

    dormlog_spark()
