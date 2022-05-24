# Generated by Django 4.0.4 on 2022-05-18 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_CourseTeachers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Обновлена')),
                ('deleted', models.BooleanField(default=False)),
                ('link_to_map', models.CharField(max_length=1024, verbose_name='Ссылка на карту')),
                ('city', models.CharField(max_length=128, verbose_name='Город')),
                ('phone', models.BigIntegerField(verbose_name='Телефон')),
                ('email', models.CharField(max_length=256, verbose_name='email')),
                ('adress', models.CharField(max_length=1024, verbose_name='Адрес')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]