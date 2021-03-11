### Тестовое задание по разработки сервиса загрузки изображений
#### Запуск локально
```
git clone https://github.com/markdrrr/picture_service.git
cd picture_service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Перейти на http://localhost:8000
```

#### Реализован функционал:
1. Загрузка изображений по ссылке либо через форму
2. Изменение размеров уже загруженных изображений.

Код покрыт тестами.
