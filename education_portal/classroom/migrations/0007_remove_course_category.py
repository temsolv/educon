# Generated by Django 3.1.5 on 2024-05-08 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_course_quizzes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
    ]
