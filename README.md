<div align="center">
<h1> api_yamdb </h1>
<p><em> Командный проект на Django Rest Framework</em></p>
</div>


▌ Описание ℹ️

**api_yamdb** — это RESTful API для веб-приложения, предназначенного для работы с отзывами на произведения. 
Реализован функционал создания, редактирования и удаления отзывов, размещение комментариев и оценок.
Приложение разработано согласно документации redoc.


В проекте применены:
- кастомная JWT аутентификация на базе djoser
- кастомная модель пользователя на базе AbstractUser


---

▌ Установка и запуск 🛠️


1. Загрузите файлы проекты.

2. Создайте виртуальное окружение и установите зависимости:  
   ```bash
   python -m venv venv
   ```

   Для Windows:
   ```bash
   venv\Scripts\activate
   ```  
   Для macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

   ```bash
   pip install -r requirements.txt
   ```

3. Выполните миграции:  
   ```bash
   python manage.py migrate
   ```

4. Создайте суперюзера:

   ```bash
   python manage.py createsuperuser  # выполните все действия'
   ```


5. Наполнитe базу данных тестовыми данными

   ```
   bash static/data/load_data.sh 
   ```

6. Запустить сервер:  
   ```bash
   python manage.py runserver
   ```

После запуска документация redoc будет доступна по ссылке:  
   [http://127.0.0.1:8000/redoc/]

   Документация swagger с воможностью отправки запросов:
   [http://127.0.0.1:8000/api/docs/]


▌ Авторы 📝

* [Виталий Воробьев](https://github.com/VitalyVorobiev)
* [Дмитрий Александров](https://github.com/DmitryAlexandrov91)
* [Михаил Тун](https://github.com/ktunec5)