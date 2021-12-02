# dormlog——web日志统计

基于 Spark Streaming，Kafka 和 HDFS 的 web 日志统计。

简单统计了状态码，客户端设备和请求次数最多的前十 IP 地址。

## 安装使用

1. 克隆该仓库
2. 下载以下软件包并放到tools目录中**（注意版本）**
   - apache-zookeeper-3.7.0-bin.tar.gz：https://zookeeper.apache.org/releases.html
   - jdk-8u311-linux-x64.tar.gz：https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html
   - hadoop-3.2.1.tar.gz：https://hadoop.apache.org/releases.html
   - spark-2.4.7-bin-hadoop2.7.tgz：https://spark.apache.org/downloads.html
   - kafka_2.11-2.4.1.tgz：http://kafka.apache.org/downloads
   - spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar：https://search.maven.org/artifact/org.apache.spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.7/jar
4. 运行 `bash build_up.sh`
5. 浏览器访问 `http://localhost:31089` 和 `http://localhost:31090` 分别可以查看 HDFS 和 Spark 节点的状态
5. 运行 `bash get_stat.sh` 可以查看统计数据，统计结果存放在 HDFS 上的 `/dormlog_project/stat_*.txt` 文件中
6. 运行 `bash down.sh clean` 来删除节点和镜像

