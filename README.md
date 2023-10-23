#  Проект «Foodgram»

## Описание проекта:

Проект Foodgram позволяет пользователям посмотреть рецепты приготовления еды, 
добавить свои рецепты, скачать ингредиенты для покупки в магазине.

![2023-10-23_10-22_2](https://github.com/VladimirChernyy/foodgram-project-react/assets/116533449/a5b82aaa-490d-4bd2-9182-d2eb7a98ea32)
![2023-10-23_10-22_1](https://github.com/VladimirChernyy/foodgram-project-react/assets/116533449/abe1daca-8f99-4d3c-a713-3b4f16e6939c)
![2023-10-23_10-22](https://github.com/VladimirChernyy/foodgram-project-react/assets/116533449/144a6e9e-e131-458d-bfbc-df39d4123688)
![2023-10-23_10-21_2](https://github.com/VladimirChernyy/foodgram-project-react/assets/116533449/a6a88bb3-ae6c-4ddd-934f-05b97ee87f29)
![2023-10-23_10-21_1](https://github.com/VladimirChernyy/foodgram-project-react/assets/116533449/e924bded-45a0-4dab-b911-bf88faab525e)
![2023-10-23_10-21](https://github.com/VladimirChernyy/foodgram-project-react/assets/116533449/8ea9a0f9-fbd4-451e-b685-d42ad2176a76)
![2023-10-23_10-20](https://github.com/VladimirChernyy/foodgram-project-react/assets/116533449/21f5936d-cfe8-497a-9898-ddc1417b270b)


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

![main.yml](https://github.com/VladimirChernyy/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Над проектом работал:
[Vladimir Chernyy](https://github.com/VladimirChernyy)
