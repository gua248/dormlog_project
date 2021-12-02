#!/bin/bash

IMAGE_NAME="dormlog_image"
echo "building image ${IMAGE_NAME}"
docker build -t="${IMAGE_NAME}" .

docker-compose up -d

sleep 3

docker exec node1 start-zookeeper.sh
docker exec node2 start-zookeeper.sh
docker exec node3 start-zookeeper.sh

docker exec node3 start-hdfs-kafka.sh
docker exec node1 start-hdfs-kafka.sh
docker exec node2 start-hdfs-kafka.sh

docker exec node1 start-spark.sh
docker exec node2 start-spark.sh
docker exec node3 start-spark.sh

docker exec node1 start-dormlog.sh
