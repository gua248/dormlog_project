#!/bin/bash

if [[ $NODE_ID == "1" ]]; then
    echo "==== start spark master ===="
    $SPARK_HOME/sbin/start-master.sh
fi

echo "==== start spark slave ===="
$SPARK_HOME/sbin/start-slave.sh spark://node1:7077

#mongod -f /data/mongodb/mongodb.conf
