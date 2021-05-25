# COMTEK
Устанавливаем postgresql по инструкции
[Инструкция](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04-ru) 
со следующими параметрами
- Имя пользователя: comtek
- Пароль: comtek
- Название базы данных: comtek


Обновляем репозитории
```sh
apt-get update
```
Устанавливаем pipenv
```sh
apt install pipenv
```
Создаём виректорию и слонируем в неё репозиторий с gitgub
```sh
cd /home
mkdir comtek && cd comtek
git clone https://github.com/Bagumg/COMTEK.git .
```
Устанавливаем зависимости и запускаем оболочку виртуального окружения
```sh
pipenv install --deploy
```
Создаём миграции djnago, применяем их и запускаем сервер
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

По адресу (http://127.0.0.1:8000/swagger/) - будет Swagger UI с описанием API и возможностью потестировать
По адресу (http://127.0.0.1:8000/admin/) - будет административная панель с возможностью создавать/просматривать/редактировать и удалять справочники и элементы
