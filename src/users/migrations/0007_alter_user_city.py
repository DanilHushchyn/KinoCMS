# Generated by Django 5.0.6 on 2024-05-20 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(choices=[('інше', 'Інше'), ('київ', 'Київ'), ('харків', 'Харків'), ('одеса', 'Одеса'), ('дніпро', 'Дніпро'), ('донецьк', 'Донецьк'), ('запоріжжя', 'Запоріжжя'), ('львів', 'Львів'), ('кривий ріг', 'Кривий Ріг'), ('миколаїв', 'Миколаїв'), ('вінниця', 'Вінниця'), ('луганськ', 'Луганськ'), ('сімферополь', 'Сімферополь'), ('херсон', 'Херсон'), ('полтава', 'Полтава'), ('чернігів', 'Чернігів'), ('черкаси', 'Черкаси'), ('житомир', 'Житомир'), ('суми', 'Суми'), ('хмельницький', 'Хмельницький'), ('чернівці', 'Чернівці'), ('рівне', 'Рівне'), ('івано-франківськ', 'Івано-Франківськ'), ('тернопіль', 'Тернопіль'), ('луцьк', 'Луцьк')], default=0, max_length=255),
        ),
    ]
