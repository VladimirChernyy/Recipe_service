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
Клонируйте с GitHub проект и перейдите в директорию проекта.
``` 
git@github.com:VladimirChernyy/foodgram-project-react.git

cd foodgram-project-react
``` 
Генерируем новый секретный ключ Django

```
sudo docker compose -f docker-compose.yml exec backend python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
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
Перейдите директорию infra:

```
cd infra
```

Соберите и запустите контейнеры в фоновом режиме
```
sudo docker compose -f docker-compose.yml up -d
```
Примените миграции
```
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
```
Соберите статику
```
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
```

Создайте суперпользователся
```
sudo docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

Загрузите игредиенты 
```
sudo docker compose -f docker-compose.yml exec backend python manage.py load_data
```

## Над проектом работал:
[Vladimir Chernyy](https://github.com/VladimirChernyy)
