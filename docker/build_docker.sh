#!/bin/bash

echo "*** Config system ***"

echo "--- Make docker image ---"

docker build -t docker_server .

echo "--- Set a alias to docker  ---"

echo "127.0.0.1 inventory" | sudo tee -a /etc/hosts

echo "--- Making container ---"

docker run -d -P --name intentory -p 2221:22 -p 8080:80 docker_server

echo "--- Set permissions to public key ---"

chmod 0600 ../Keys/key

echo "--- Register container on SSH known_hosts  ---"

ssh -o StrictHostKeyChecking=no root@inventory -p 2221 -i ../Keys/key hostname

echo "*** Container Done ***"
