# О проекте
Целью проекта являлась разработка системы управления обучением. Основной функционал системы:

 - Создание учебных курсов
 - Наполнение курсов контентом
 - Распределение курсов по пользователям
 - Возможность пройти курс

# Запуск
Вместе с сервером необходимо запускать фоновые задачи:
```python
python manage.py process_tasks
python manage.py runserver
```
