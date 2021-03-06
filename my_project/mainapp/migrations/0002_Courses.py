# Generated by Django 4.0.4 on 2022-05-18 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_News'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='Обновлена')),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('description_as_markdown', models.BooleanField(default=False, verbose_name='Markdown')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Цена')),
                ('cover', models.CharField(default='no_image.svg', max_length=25, verbose_name='Изображение')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
