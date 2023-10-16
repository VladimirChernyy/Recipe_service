#  Проект «Foodgram»

## Описание проекта:

Проект Foodgram позволяет пользователям посмотреть рецепты приготовления еды, 
добавить свои рецепты, скачать ингредиенты для покупки в магазине.


## В проекте были использованы технологии:
Django REST
Python 3.9
Gunicorn
Nginx
JS
Node.js
PostgreSQL
Docker

## Попробовать демо-версию:
* [Foodgram](https://ya-foodgramm.ddns.net)
---

## Как запустить проект:



 Настраиваем Docker
``` 
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin;
``` 
Создайте и перейдите в директорию проекта.
``` 
mkdir foodgram && cd foodgram
``` 
Генерируем новый секретный ключ Django

```
sudo docker compose -f docker-compose.production.yml exec backend python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Создаем файл .env, в котором нужно указать данные

``` 
sudo nano .env
```
Добавьте в файл .env код  

```
DJANGO_KEY=<Сгенерированный_ключ>
POSTGRES_DB=<Желаемое_имя_базы_данных>
POSTGRES_USER=<Желаемое_имя_пользователя_базы_данных>
POSTGRES_PASSWORD=<Желаемый_пароль_пользователя_базы_данных>
DB_HOST=db
DB_PORT=5432
```
Скопируйте папку с локального сервера на удаленный:

```
scp -r infra/* <server_user>@<server_IP>:/home/<server_user>/foodgram/
```

Соберите и запустите контейнеры в фоновом режиме
```
sudo docker compose -f docker-compose.production.yml up -d
```
Примените миграции
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
Соберите статику
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

Создайте суперпользователся
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```



Устанавливаем NGINX
```
sudo apt install nginx -y
```
Запускаем NGINX
```
sudo systemctl start nginx
```
Настраиваем firewall
```
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
```
Включаем firewall
```
sudo ufw enable
```
Откройте конфигурационный файл NGINX
```
sudo nano /etc/nginx/sites-enabled/default
```
Добавьте настройки:
```
server {
    server_name 62.84.123.251 ya-foodgramm.ddns.net;

    location / {
        proxy_set_header        Host $host;
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8088;
    }

```

Проверяем корректность настроек
```
sudo nginx -t
```
Запускаем NGINX
```
sudo systemctl start nginx
```

Настройте HTTPS


Установите пакетный менеджер snap.
```
sudo apt install snapd
```
Установите и обновите зависимости для пакетного менеджера snap.
```
sudo snap install core; sudo snap refresh core
```
Установите пакет certbot.
```
sudo snap install --classic certbot
```
Создайте ссылку на certbot в системной директории, чтобы у пользователя с правами администратора был доступ к этому пакету.
sudo ln -s /snap/bin/certbot /usr/bin/certbot

Получите сертификат 
```
sudo certbot --nginx
```
Перезапустите NGINX
```
sudo systemctl reload nginx
```

## Над проектом работал:
[Vladimir Chernyy](https://github.com/VladimirChernyy)
