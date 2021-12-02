#!/bin/bash

docker-compose down

if [[ $1 == "clean" ]]; then
    IMAGE_NAME="dormlog_image"
    echo "removing image $IMAGE_NAME"
    docker rmi $IMAGE_NAME
fi
