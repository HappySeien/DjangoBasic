# Generated by Django 4.0.4 on 2022-05-29 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
