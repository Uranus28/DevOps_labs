#!/bin/bash -x

# Удаляем старый контейнер если есть
docker stop nginx-cont
docker rm   nginx-cont

# собираем образ
docker build -t devops/nginx-server ./nginx

# Создаем и собираем контейнер
docker run -d --name nginx-cont -p 54321:80 --restart unless-stopped devops/nginx-server

# Проверяемм
docker ps -a
sleep 5
curl 127.0.0.1:54321
docker logs -n 10 nginx-cont