#!/bin/bash

sudo docker build -t test-app . && \
sudo docker run --rm -it --name task2 -p 5000:5000 test-app && \
sudo docker rmi test-app
