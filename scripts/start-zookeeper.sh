#!/bin/bash

echo "==== start zookeeper ===="
echo `expr $NODE_ID` > $ZOOKEEPER_HOME/data/myid
zkServer.sh start
/usr/sbin/sshd
