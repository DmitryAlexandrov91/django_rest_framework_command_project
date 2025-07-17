<div align="center">
<h1> api_yamdb </h1>
<p><em> Командный проект на Django Rest Framework</em></p>
</div>


▌ Описание ℹ️

**api_yamdb** — это RESTful API для веб-приложения, предназначенного для работы с отзывами на произведения. 
Реализован функционал создания, редактирования и удаления отзывов, размещение комментариев и оценок.
Приложение разработано согласно документации redoc.


В проекте применены:
- кастомная JWT авторизация на базе djoser
- кастомная модель пользователя на базе AbstractUser


## Требования

* Операционная система: Windows 10 или выше
* Язык программирования: Python 3.9 или выше

## Использованные технологии

* Python 3.9
* Django REST framework
* Валидация данных
* Simple JWT


## Установка

1. Склонировать репозиторий:  
   ```bash
   git clone https://github.com/ktunec5/api_yamdb
   ```
2. Создать виртуальное окружение:  
   ```bash
   python -m venv venv
   ```
3. Активировать виртуальное окружение:  
   Для Windows:
   ```bash
   venv\Scripts\activate
   ```  
   Для macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
4. Установить зависимости:  
   ```bash
   pip install -r requirements.txt
   ```
5. Обновить pip:  
   ```bash
   python -m pip install --upgrade pip
   ```
6. Выполнить миграции:  
   ```bash
   python manage.py migrate
   ```
7. Наполнить базу данных. 
   ```
   python manage.py get_data путь к файлу
   ```
   
   ВНИМАНИЕ! В первую очередь заполняются таблицы, где нет полей связи с другими таблицами.
   Записывайте данные в следующем порядке:
   1. customuser, category, genre
   2. title
   3. genretitle, review, comment

   Пример:
   ```bash
   python manage.py get_data static/data/customuser.csv
   python manage.py get_data static/data/category.csv
   python manage.py get_data static/data/genre.csv
   ```
   Далее title:
   ```bash
   python manage.py get_data static/data/title.csv
   ```
   Далее по инструкции.

8. Запустить сервер:  
   ```bash
   python manage.py runserver
   ```
9. После запуска документация будет доступна по ссылке:  
   [http://127.0.0.1:8000/redoc/]

## Примеры запросов

### 1. Получение списка всех произведений:
**GET** `api/v1/titles/`

**Пример ответа**:
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": []
}
```

### 2. Получение отзывов на произведение:
**GET** `api/v1/titles/{title_id}/reviews/`

**Пример ответа**:
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### 3. Получение всех комментариев к отзыву:
**GET** `api/v1/titles/{title_id}/reviews/{review_id}/comments/`

**Пример ответа**:
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": []
}
```

### 4. Получение одного комментария:
**GET** `api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`

**Пример ответа**:
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

## Авторы проекта

* [Виталий Воробьев](https://github.com/VitalyVorobiev)
* [Дмитрий Александров](https://github.com/DmitryAlexandrov91)
* [Михаил Тун](https://github.com/ktunec5)