## Калькулятор
Напишем простой API-калькулятор на Flask, который принимает и обрабатывает POST-запрос от пользователя.
Также опишем необходимые зависимости в requirements.txt
Для работы использовался Ubuntu Linux 20.04

## Docker
Напишем Dockerfile для сборки и запуска контейнера, где используется базовый образ python, устанавливаются зависимости и запускается наше приложение calc.py
Для начала соберем и запустим контейнер локально
Сборка:
![image](https://github.com/user-attachments/assets/71aa72ee-ee29-45ae-b90e-6f5926fb6131)
Запуск контейнера:
![image](https://github.com/user-attachments/assets/33452894-088c-43c2-9ef3-7e436e05ca08)

Проверка работы приложения:
![image](https://github.com/user-attachments/assets/aa06f264-c073-473d-b73d-a1694a13e851)

## Развертывание gitlab
Для непрерывной интеграции нам понадобится gitlab.
Создаём docker-compose.yml для запуска контейнеров с gitlab и gitlab-runner:
`
version: '2.6'
services:
  gitlab:
    image: gitlab/gitlab-ce:16.10.0-ce.0
    container_name: gitlab
    restart: always
    hostname: 'gitlab.example.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.example.com'
    ports:
      - '80:80'
      - '443:443'
      - '22:22'
    volumes:
      - '/srv/gitlab/config:/etc/gitlab'
      - '/srv/gitlab/logs:/var/log/gitlab'
      - '/srv/gitlab/data:/var/opt/gitlab'
    shm_size: '256m'
    networks:
      - gitlab_net

  gitlab-runner:
    image: gitlab/gitlab-runner:alpine
    container_name: gitlab-runner
    restart: unless-stopped
    depends_on:
      - gitlab
    volumes:
      - /srv/gitlab-runner:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - gitlab_net

networks:
  gitlab_net:
    driver: bridge
```
Запускаем контейнеры командой ```docker compose up -d```
![image](https://github.com/user-attachments/assets/f3a7c4b6-af64-4642-8595-cb0ffb313294)

URL для перехода в gitlab через браузер: https://<ip-адрес машины>
![image](https://github.com/user-attachments/assets/74e8f0a5-647d-459d-9f2c-5cf50141cf1f)
Чтобы сбросить пароль рута и установить новый нужно выполнить следующие команды:
```
docker exec -it gitlab /bin/bash
cd /etc/gitlab
gitlab-rake "gitlab:password:reset[root]"
```
После этого можем успешно войти под именем root
![image](https://github.com/user-attachments/assets/84595657-f2a9-46a1-a17f-660ce9e0bd4e)

Заходим в Admin area, оттуда в Users, создадим пользователя с именем. Заходим в этого же пользователя, меняем пароль. После входа тоже потребуется смена.
![image](https://github.com/user-attachments/assets/d16ac4c0-1b9c-4813-ab33-474ad4a8bcb6)

Создаем группу, в которой создаем репозиторий.
![image](https://github.com/user-attachments/assets/98ec712f-5976-4379-a95f-c192e3a4e952)
![image](https://github.com/user-attachments/assets/79b1ae58-54d9-4b27-a1c9-85d944d82a9b)



Создаем ключи и сертификаты в директории /srv/gitlab/config/ssl для корректной работы раннера
```
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 3654 -key ca.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=Acme Root CA" -out ca.crt
openssl req -newkey rsa:2048 -nodes -keyout gitlab.example.com.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=*.example.com" -out gitlab.example.com.csr
openssl x509 -req -extfile <(printf "subjectAltName=DNS:example.com,DNS:www.example.com,DNS:gitlab.example.com") -days 365 -in gitlab.example.com.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out gitlab.example.com.crt
```
![image](https://github.com/user-attachments/assets/d086f312-f627-4869-8199-2c0b98273fe8)

Подкладываем в /srv/gitlab-runner ca.crt.
![image](https://github.com/user-attachments/assets/3968b38b-fa5f-4f0b-9ad1-566cf94ef9a9)

Регистрируем раннер:
```
docker exec -it gitlab-runner /bin/bash
gitlab-runner register --url "https://gitlab.example.com" --tls-ca-file=/etc/gitlab-runner/ca.crt --registration-token "<token>"
```
![image](https://github.com/user-attachments/assets/4940dddd-e7ff-4916-9d55-c265fc169839)

Token раннера необходимо создать в проекте -> Settings -> CI/CD -> Runners -> New project runner image
![image](https://github.com/user-attachments/assets/8575fd9d-06f9-42bc-9e89-0523332e58b7)

Gitlab и gitlab-runner должны находится в одной сети.

